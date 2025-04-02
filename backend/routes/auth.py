"""Authentication routes."""
from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db
import duckdb
from utils.auth import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Handle user registration."""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['username', 'password', 'email', 'name']):
            return jsonify({'error': 'Missing required fields'}), 400

        db = get_db()
        
        # Check if username already exists
        existing_user = db.execute("""
            SELECT 1 FROM users WHERE username = ?
        """, [data['username']]).fetchone()
        
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        # Get next available ID
        next_id = db.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM users").fetchone()[0]
        
        # Insert new user
        db.execute("""
            INSERT INTO users (id, username, password_hash, email, name)
            VALUES (?, ?, ?, ?, ?)
        """, (
            next_id,
            data['username'],
            generate_password_hash(data['password']),
            data['email'],
            data['name']
        ))
        
        db.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except duckdb.Error as e:
        print(f"Database error during signup: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        print(f"Error during signup: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Get database connection
        db = get_db()
        if not db:
            return jsonify({'error': 'Database connection failed'}), 503
        
        # Get user from database
        user = db.execute("""
            SELECT id, username, password_hash, email, name 
            FROM users 
            WHERE username = ?
        """, (username,)).fetchone()
        
        if user and check_password_hash(user[2], password):
            # Set session
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[3]
            session['name'] = user[4]
            
            # Set session cookie parameters
            session.permanent = True
            session.modified = True
            
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user[0],
                    'username': user[1],
                    'email': user[3],
                    'name': user[4]
                }
            })
        
        return jsonify({'error': 'Invalid username or password'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'An error occurred during login'}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user logout."""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/check_auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated."""
    return jsonify({
        'authenticated': 'user_id' in session,
        'username': session.get('username')
    }), 200 