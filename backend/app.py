"""Main Flask application."""
from flask import Flask, send_from_directory
from config.config import SECRET_KEY, STATIC_FOLDER, DEBUG, HOST, PORT
from routes.auth import auth_bp
from routes.spreadsheet import spreadsheet_bp
from extensions import socketio
import os

def create_app():
    """Create and configure the Flask application."""
    # Ensure static folder exists
    os.makedirs(STATIC_FOLDER, exist_ok=True)
    
    app = Flask(__name__, 
                static_folder=STATIC_FOLDER,
                static_url_path='')
    app.secret_key = SECRET_KEY

    # Initialize extensions
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(spreadsheet_bp)

    # Add route for root URL to serve index.html
    @app.route('/')
    def index():
        return send_from_directory(STATIC_FOLDER, 'index.html')

    # Add route for spreadsheet.html
    @app.route('/spreadsheet.html')
    def spreadsheet():
        return send_from_directory(STATIC_FOLDER, 'spreadsheet.html')

    # Add route for signup.html
    @app.route('/signup.html')
    def signup():
        return send_from_directory(STATIC_FOLDER, 'signup.html')

    print(f"Static folder path: {STATIC_FOLDER}")
    print(f"Static folder exists: {os.path.exists(STATIC_FOLDER)}")
    print(f"Index.html exists: {os.path.exists(os.path.join(STATIC_FOLDER, 'index.html'))}")

    return app

if __name__ == '__main__':
    print("Starting Flask server...")
    app = create_app()
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG)
