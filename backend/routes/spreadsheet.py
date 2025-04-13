"""Spreadsheet routes."""

from flask import Blueprint, jsonify, request, session

from backend.extensions import socketio
from backend.utils.auth import login_required
from database.db import get_db
from database.redis_client import get_queue_status, get_redis

spreadsheet_bp = Blueprint("spreadsheet", __name__)


def broadcast_update():
    """Broadcast queue status to all clients."""
    try:
        redis_client = get_redis()
        if not redis_client:
            return

        current_lock = redis_client.get("write_lock")
        queue = redis_client.lrange("write_queue", 0, -1)

        # Send queue status to all clients
        for client in socketio.server.eio.clients:
            username = client.get("username")
            if username:
                position = None
                if current_lock == username:
                    position = 0
                elif username in queue:
                    position = queue.index(username) + 1
                socketio.emit(
                    "queue_update", {"position": position}, room=client.get("sid")
                )
    except Exception as e:
        print(f"Error broadcasting update: {e!s}")


@spreadsheet_bp.route("/read_data")
@login_required
def read_data_with_queue():
    """Read data from the spreadsheet with queue status."""
    try:
        db = get_db()
        redis = get_redis()

        # Get sales data
        sales_data = db.execute("""
            SELECT date, invoice_number, customer_name, location, 
                   product_name, category, volume_sold, unit, created_by
            FROM sales
            ORDER BY date DESC, invoice_number DESC
        """).fetchall()

        # Get categories
        categories = db.execute("""
            SELECT name, description
            FROM categories
            ORDER BY name
        """).fetchall()

        # Get queue status
        active_users, queue_users = get_queue_status(redis)

        return jsonify(
            {
                "sales_data": sales_data,
                "categories": categories,
                "active_users": active_users,
                "queue_users": queue_users,
            }
        )
    except Exception as e:
        print(f"Error reading data: {e!s}")
        return jsonify({"error": str(e)}), 500


@spreadsheet_bp.route("/write", methods=["POST"])
def write_data():
    """Write data to the spreadsheet."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required_fields = [
            "date",
            "invoice_number",
            "customer_name",
            "location",
            "product_name",
            "category",
            "volume_sold",
            "unit",
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Get the current user from session
        username = session.get("username")
        if not username:
            return jsonify({"error": "Not authenticated"}), 401

        # Get the next ID
        db = get_db()
        cursor = db.execute("SELECT MAX(id) FROM sales")
        max_id = cursor.fetchone()[0]
        next_id = (max_id or 0) + 1

        # Insert the new sale
        db.execute(
            """
            INSERT INTO sales (
                id, date, invoice_number, customer_name, location,
                product_name, category, volume_sold, unit, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                next_id,
                data["date"],  # Use the date directly from the request
                data["invoice_number"],
                data["customer_name"],
                data["location"],
                data["product_name"],
                data["category"],
                data["volume_sold"],
                data["unit"],
                username,
            ),
        )
        db.commit()

        # Broadcast the update to all connected clients
        socketio.emit("data_updated", {"message": "Data updated"})

        return jsonify({"message": "Data written successfully"})

    except Exception as e:
        print(f"Error writing data: {e!s}")
        return jsonify({"error": str(e)}), 500


@socketio.on("request_write_access")
def handle_write_access_request(data):
    """Handle write access request from a user."""
    try:
        username = data.get("username")
        if not username:
            return {"success": False, "message": "Username is required"}

        redis_client = get_redis()
        if not redis_client:
            return {"success": False, "message": "Failed to connect to Redis"}

        # Check if user already has write access
        current_lock = redis_client.get("write_lock")
        if current_lock == username:
            # User already has access, extend the lock
            redis_client.expire("write_lock", 60)  # 60 seconds timeout
            return {"success": True, "message": "Write access extended"}

        # Check if any user has write access
        if current_lock:
            # Add user to queue if not already in it
            if username not in redis_client.lrange("write_queue", 0, -1):
                redis_client.rpush("write_queue", username)
            queue_position = redis_client.llen("write_queue")
            return {
                "success": False,
                "message": (
                    f"Write access is currently held by another user. "
                    f"You are #{queue_position} in queue"
                ),
            }

        # No one has write access, grant it to this user
        redis_client.set("write_lock", username)
        redis_client.expire("write_lock", 60)  # 60 seconds timeout
        return {"success": True, "message": "Write access granted"}
    except Exception as e:
        print(f"Error handling write access request: {e!s}")
        return {"success": False, "message": str(e)}


@socketio.on("release_write_access")
def handle_write_access_release(data):
    """Handle write access release from a user."""
    try:
        username = data.get("username")
        if not username:
            return {"success": False, "message": "Username is required"}

        redis_client = get_redis()
        if not redis_client:
            return {"success": False, "message": "Failed to connect to Redis"}

        # Check if user has write access
        current_lock = redis_client.get("write_lock")
        if current_lock != username:
            return {"success": False, "message": "You do not have write access"}

        # Release write access
        redis_client.delete("write_lock")

        # Get next user in queue
        next_user = redis_client.lpop("write_queue")
        if next_user:
            # Grant write access to next user
            redis_client.set("write_lock", next_user)
            redis_client.expire("write_lock", 10)  # 10 seconds timeout
            # Broadcast update to all clients
            broadcast_update()
            return {
                "success": True,
                "message": f"Write access released and granted to {next_user}",
            }

        # Broadcast update to all clients
        broadcast_update()
        return {"success": True, "message": "Write access released"}
    except Exception as e:
        print(f"Error handling write access release: {e!s}")
        return {"success": False, "message": str(e)}


@spreadsheet_bp.route("/read")
def read_data():
    try:
        db = get_db()

        # Get all sales data
        cursor = db.execute("""
            SELECT strftime('%Y-%m-%d', date) as date, 
                   invoice_number, 
                   customer_name, 
                   location, 
                   product_name, 
                   category, 
                   volume_sold, 
                   unit, 
                   created_by
            FROM sales
            ORDER BY date DESC, id DESC
        """)
        sales_data = cursor.fetchall()

        # Get all categories from the categories table
        cursor = db.execute("""
            SELECT name FROM categories 
            ORDER BY name
        """)
        categories = cursor.fetchall()

        # If no categories exist, insert default categories
        if not categories:
            db.execute("""
                INSERT INTO categories (name, description) VALUES
                    ('Water', 'Bottled water and mineral water'),
                    ('Juice', 'Fruit juices and juice drinks'),
                    ('Soda', 'Carbonated soft drinks'),
                    ('Energy Drinks', 'Energy and sports drinks'),
                    ('Tea', 'Bottled and canned tea'),
                    ('Coffee', 'Bottled and canned coffee'),
                    ('Milk', 'Dairy milk and milk-based drinks'),
                    ('Dairy', 'Other dairy products like yogurt drinks and kefir'),
                    ('Alcohol', 'Alcoholic beverages'),
                    ('Other', 'Other types of beverages')
            """)
            db.commit()
            # Fetch categories again after inserting defaults
            cursor = db.execute("SELECT name FROM categories ORDER BY name")
            categories = cursor.fetchall()

        return jsonify({"sales_data": sales_data, "categories": categories})

    except Exception as e:
        print(f"Error reading data: {e!s}")
        return jsonify({"error": str(e)}), 500
