"""Authentication utility functions."""
import hashlib
import secrets
from functools import wraps
from flask import session, jsonify

def hash_password(password, salt=None):
    """Hash password with salt."""
    if salt is None:
        salt = secrets.token_hex(8)
    hash_obj = hashlib.sha256()
    hash_obj.update((password + salt).encode())
    return hash_obj.hexdigest(), salt

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function 