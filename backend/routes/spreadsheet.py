"""Spreadsheet routes."""
from flask import Blueprint, jsonify, request, session
from database.db import get_db
from database.redis_client import get_redis, request_write_access, check_write_access, release_write_access, get_queue_status
from utils.auth import login_required
from extensions import socketio

spreadsheet_bp = Blueprint('spreadsheet', __name__)

def broadcast_update():
    """Broadcast updates to all connected clients."""
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
        
        socketio.emit('data_update', {
            'sales_data': sales_data,
            'categories': categories,
            'active_users': active_users,
            'queue_users': queue_users
        }, broadcast=True)
    except Exception as e:
        print(f"Error broadcasting update: {str(e)}")

@spreadsheet_bp.route('/read_data')
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
        
        return jsonify({
            'sales_data': sales_data,
            'categories': categories,
            'active_users': active_users,
            'queue_users': queue_users
        })
    except Exception as e:
        print(f"Error reading data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@spreadsheet_bp.route('/write', methods=['POST'])
def write_data():
    """Write data to spreadsheet."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get Redis client
        redis_client = get_redis()
        if not redis_client:
            return jsonify({'error': 'Redis is not available'}), 503
        
        # Get username from session
        username = session.get('username')
        if not username:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Check write access
        has_access, message = check_write_access(redis_client, username)
        if not has_access:
            return jsonify({'error': message}), 403
        
        # Get database connection
        db = get_db()
        if not db:
            return jsonify({'error': 'Database connection failed'}), 503
        
        # Start transaction
        db.execute("BEGIN TRANSACTION")
        
        try:
            # Get the next available ID
            next_id = db.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM sales").fetchone()[0]
            
            # Insert new sale
            db.execute("""
                INSERT INTO sales (
                    id, date, invoice_number, customer_name, location, 
                    product_name, category, volume_sold, unit, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                next_id,
                data.get('date'),
                data.get('invoice_number'),
                data.get('customer_name'),
                data.get('location'),
                data.get('product_name'),
                data.get('category'),
                data.get('volume_sold'),
                data.get('unit'),
                username
            ))
            
            # Commit transaction
            db.execute("COMMIT")
            
            # Broadcast update to all clients
            try:
                socketio.emit('data_updated', {'message': 'Data updated successfully'})
            except Exception as e:
                print(f"Error broadcasting update: {str(e)}")
            
            return jsonify({'message': 'Sale added successfully'})
            
        except Exception as e:
            # Rollback transaction on error
            db.execute("ROLLBACK")
            raise e
            
    except Exception as e:
        print(f"Error writing data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@spreadsheet_bp.route('/request_write_access', methods=['POST'])
def handle_write_access_request():
    """Request write access."""
    try:
        username = session.get('username')
        if not username:
            return jsonify({'error': 'Not authenticated'}), 401
        
        redis_client = get_redis()
        if not redis_client:
            return jsonify({'error': 'Redis is not available'}), 503
        
        has_access, message = request_write_access(redis_client, username)
        return jsonify({
            'has_access': has_access,
            'message': message
        })
    except Exception as e:
        print(f"Error requesting write access: {str(e)}")
        return jsonify({'error': str(e)}), 500

@spreadsheet_bp.route('/release_write_access', methods=['POST'])
def handle_write_access_release():
    """Release write access."""
    try:
        username = session.get('username')
        if not username:
            return jsonify({'error': 'Not authenticated'}), 401
        
        redis_client = get_redis()
        if not redis_client:
            return jsonify({'error': 'Redis is not available'}), 503
        
        success, message = release_write_access(redis_client, username)
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        print(f"Error releasing write access: {str(e)}")
        return jsonify({'error': str(e)}), 500

@spreadsheet_bp.route('/read', methods=['GET'])
def read_data():
    """Read data from spreadsheet."""
    try:
        db = get_db()
        if not db:
            return jsonify({'error': 'Database connection failed'}), 503
        
        # Get categories
        categories = db.execute("SELECT name FROM categories").fetchall()
        
        # Get sales data
        sales_data = db.execute("""
            SELECT date, invoice_number, customer_name, location, 
                   product_name, category, volume_sold, unit, created_by
            FROM sales
            ORDER BY date DESC
        """).fetchall()
        
        return jsonify({
            'categories': categories,
            'sales_data': sales_data
        })
    except Exception as e:
        print(f"Error reading data: {str(e)}")
        return jsonify({'error': str(e)}), 500 