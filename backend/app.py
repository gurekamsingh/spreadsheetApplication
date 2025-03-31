print("Flask app is starting...")
from flask import Flask, request, jsonify, session, send_from_directory
import duckdb
import threading
import hashlib
import secrets
import os
import traceback
from datetime import datetime

app = Flask(__name__, static_folder='../frontend')
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key

# Try to import and connect to Redis, but don't fail if it's not available
try:
    import redis
    r = redis.Redis(host='localhost', port=6380, decode_responses=True, socket_timeout=5)
    r.ping()  # Test the connection
    print("Successfully connected to Redis")
    REDIS_AVAILABLE = True
except (ImportError, redis.ConnectionError) as e:
    print(f"Warning: Redis is not available. Some features will be limited. Error: {str(e)}")
    r = None
    REDIS_AVAILABLE = False
except Exception as e:
    print(f"Unexpected error connecting to Redis: {str(e)}")
    r = None
    REDIS_AVAILABLE = False

# Lock mechanism
LOCK_KEY = "spreadsheet_lock"
ACTIVE_USERS_KEY = "active_users"
WRITE_QUEUE_KEY = "write_queue"  # New key for tracking write access queue

# Create database directory if it doesn't exist
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'spreadsheet.db')
print(f"Database path: {DB_PATH}")

def get_db():
    if not hasattr(app, 'db'):
        print(f"Creating new database connection at {DB_PATH}")
        app.db = duckdb.connect(DB_PATH)
        print("Creating tables if they don't exist...")
        
        # Drop the existing sheet table if it exists to ensure clean schema
        app.db.execute("DROP TABLE IF EXISTS sheet")
        
        # Create sheet table with all required columns
        app.db.execute("""
            CREATE TABLE sheet (
                id INTEGER,
                data TEXT,
                user TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Drop the existing users table if it exists to ensure clean schema
        app.db.execute("DROP TABLE IF EXISTS users")
        
        # Create users table with all required columns
        app.db.execute("""
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tables created successfully")
    return app.db

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(8)
    hash_obj = hashlib.sha256()
    hash_obj.update((password + salt).encode())
    return hash_obj.hexdigest(), salt

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/signup.html')
def serve_signup():
    return send_from_directory(app.static_folder, 'signup.html')

@app.route('/spreadsheet.html')
def serve_spreadsheet():
    return send_from_directory(app.static_folder, 'spreadsheet.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')

        print(f"Signup attempt for username: {username}, email: {email}, name: {name}")

        if not all([username, email, name, password]):
            return jsonify({"error": "All fields are required"}), 400

        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400

        db = get_db()
        
        # Check if username or email already exists
        print("Checking for existing username/email...")
        result = db.execute("SELECT username, email FROM users WHERE username = ? OR email = ?", 
                          [username, email]).fetchone()
        if result:
            if result[0] == username:
                print(f"Username {username} already exists")
                return jsonify({"error": "Username already exists"}), 400
            else:
                print(f"Email {email} already registered")
                return jsonify({"error": "Email already registered"}), 400

        # Hash password and store user
        password_hash, salt = hash_password(password)
        print("Inserting new user into database...")
        db.execute("""
            INSERT INTO users (username, email, name, password_hash, salt) 
            VALUES (?, ?, ?, ?, ?)
        """, [username, email, name, password_hash, salt])
        
        # Verify the insertion
        verify = db.execute("SELECT username, email, name FROM users WHERE username = ?", [username]).fetchone()
        print(f"User data verified: {verify}")
        
        print(f"Successfully created user: {username}")
        return jsonify({"message": "User created successfully"})
    except Exception as e:
        print(f"Error during signup: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": "Failed to create user. Please try again."}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')

        print(f"Login attempt for username: {username}")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        db = get_db()
        print("Checking user credentials...")
        result = db.execute("SELECT password_hash, salt FROM users WHERE username = ?", [username]).fetchone()
        
        if not result:
            print(f"User not found: {username}")
            return jsonify({"error": "Invalid username or password"}), 401

        password_hash, salt = result
        if hash_password(password, salt)[0] != password_hash:
            print(f"Invalid password for user: {username}")
            return jsonify({"error": "Invalid username or password"}), 401

        session['username'] = username
        print(f"Successfully logged in user: {username}")
        return jsonify({"message": "Login successful"})
    except Exception as e:
        print(f"Error during login: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": "Login failed. Please try again."}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully"})

@app.route('/check_auth', methods=['GET'])
def check_auth():
    if 'username' in session:
        return jsonify({"authenticated": True, "username": session['username']})
    return jsonify({"authenticated": False})

@app.route('/request_write', methods=['POST'])
def request_write():
    if 'username' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    if not REDIS_AVAILABLE:
        return jsonify({"error": "Real-time features are not available. Please try again later."}), 503
    
    user = session['username']
    current_lock = r.get(LOCK_KEY)
    
    if current_lock:
        if current_lock == user:
            # User already has the lock, extend it
            r.set(LOCK_KEY, user, ex=30)
            r.sadd(ACTIVE_USERS_KEY, user)  # Ensure user is in active users set
            return jsonify({"message": "Write access maintained"})
        else:
            # Add user to queue if not already in it
            if not r.sismember(WRITE_QUEUE_KEY, user):
                r.sadd(WRITE_QUEUE_KEY, user)
                # Get user's position in queue
                queue_position = r.scard(WRITE_QUEUE_KEY)
                return jsonify({
                    "error": f"User {current_lock} is currently editing. You are #{queue_position} in line.",
                    "queue_position": queue_position
                }), 403
            else:
                # Get user's position in queue
                queue_position = r.scard(WRITE_QUEUE_KEY)
                return jsonify({
                    "error": f"You are #{queue_position} in line for write access.",
                    "queue_position": queue_position
                }), 403
    
    # No one has the lock, check queue
    next_user = r.spop(WRITE_QUEUE_KEY)
    if next_user and next_user != user:
        # Someone else was waiting first
        r.sadd(WRITE_QUEUE_KEY, next_user)  # Put them back in queue
        queue_position = r.scard(WRITE_QUEUE_KEY)
        return jsonify({
            "error": f"User {next_user} was waiting first. You are #{queue_position} in line.",
            "queue_position": queue_position
        }), 403
    
    # Grant access to current user
    r.set(LOCK_KEY, user, ex=30)
    r.sadd(ACTIVE_USERS_KEY, user)  # Add user to active users set
    return jsonify({"message": "Write access granted!"})

@app.route('/write_data', methods=['POST'])
def write_data():
    if 'username' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    if not REDIS_AVAILABLE:
        return jsonify({"error": "Real-time features are not available. Please try again later."}), 503
    
    user = session['username']
    data = request.json.get('data')
    title = request.json.get('title', 'Untitled')

    current_lock = r.get(LOCK_KEY)
    if not current_lock:
        return jsonify({"error": "Write access not requested. Please request write access first."}), 403
    
    if current_lock != user:
        return jsonify({"error": f"User {current_lock} is currently editing the spreadsheet. Please wait."}), 403

    try:
        # Save data to DuckDB with current timestamp
        db = get_db()
        db.execute("""
            INSERT INTO sheet (id, data, user, timestamp) 
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (1, f"{title}\n{data}", user))

        # Publish update to Redis Stream
        r.xadd("spreadsheet_updates", {
            "data": f"{title}\n{data}", 
            "user": user,
            "timestamp": str(datetime.now())
        })

        # Extend the lock
        r.set(LOCK_KEY, user, ex=30)
        return jsonify({"message": "Data saved successfully!"})
    except Exception as e:
        print(f"Error during write: {str(e)}")
        return jsonify({"error": "Failed to save data. Please try again."}), 500

@app.route('/read_data', methods=['GET'])
def read_data():
    if not REDIS_AVAILABLE:
        return jsonify({"error": "Real-time features are not available. Please try again later."}), 503
    
    try:
        # Get the latest data from DuckDB
        db = get_db()
        result = db.execute("""
            SELECT data, user, timestamp 
            FROM sheet 
            ORDER BY id DESC, timestamp DESC 
            LIMIT 1
        """).fetchone()
        
        latest_data = result[0] if result else None
        last_user = result[1] if result else None
        last_update = result[2] if result else None
        
        # Get active users and queue
        current_lock = r.get(LOCK_KEY)
        active_users = [current_lock] if current_lock else []  # Only the user with lock is active
        queue_users = list(r.smembers(WRITE_QUEUE_KEY))
        
        return jsonify({
            "data": latest_data,
            "active_users": active_users,
            "queue_users": queue_users,
            "last_user": last_user,
            "last_update": last_update
        })
    except Exception as e:
        print(f"Error reading data: {str(e)}")
        return jsonify({"error": "Failed to read data"}), 500

@app.route('/release_lock', methods=['POST'])
def release_lock():
    if 'username' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    if not REDIS_AVAILABLE:
        return jsonify({"error": "Real-time features are not available. Please try again later."}), 503
    
    user = session['username']
    current_lock = r.get(LOCK_KEY)
    
    if current_lock == user:
        # Remove lock and user from active users
        r.delete(LOCK_KEY)
        r.srem(ACTIVE_USERS_KEY, user)
        
        # Check if there are users in queue
        next_user = r.spop(WRITE_QUEUE_KEY)
        if next_user:
            # Grant access to next user in queue
            r.set(LOCK_KEY, next_user, ex=30)
            r.sadd(ACTIVE_USERS_KEY, next_user)
        
        return jsonify({"message": "Lock released!"})
    else:
        return jsonify({"error": "You do not own the lock!"}), 403

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
