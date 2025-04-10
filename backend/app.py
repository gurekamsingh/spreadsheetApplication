"""Main Flask application."""
from flask import Flask, send_from_directory
from config.config import SECRET_KEY, STATIC_FOLDER, DEBUG, HOST, PORT
from routes.auth import auth_bp
from routes.spreadsheet import spreadsheet_bp
from extensions import socketio
import os
import sys
from pathlib import Path

# Add the root directory to the Python path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

def create_app():
    """Create and configure the Flask application."""
    # Ensure static folder exists
    os.makedirs(STATIC_FOLDER, exist_ok=True)
    
    app = Flask(__name__, 
                static_folder=STATIC_FOLDER,
                static_url_path='')
    app.secret_key = SECRET_KEY

    # Initialize extensions
    socketio.init_app(app, 
                     cors_allowed_origins="*",
                     async_mode='threading',
                     ping_timeout=60,
                     ping_interval=25,
                     logger=True,
                     engineio_logger=True)

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
    
    # Get the local IP address
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"Server will be available at:")
    print(f"http://localhost:{PORT}")
    print(f"http://127.0.0.1:{PORT}")
    print(f"http://{local_ip}:{PORT}")
    
    try:
        socketio.run(app, 
                    host='127.0.0.1',  # Use localhost
                    port=PORT, 
                    debug=DEBUG,
                    allow_unsafe_werkzeug=True,
                    use_reloader=False)  # Disable reloader to prevent duplicate sockets
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        print("Make sure no other application is using port 5000")
