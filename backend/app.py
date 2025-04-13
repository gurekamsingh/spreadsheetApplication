"""Flask application factory."""

import os
import socket

from flask import Flask

from .config.config import DEBUG, HOST, PORT
from .extensions import socketio
from .routes.auth import auth_bp
from .routes.spreadsheet import spreadsheet_bp


def create_app(testing=False):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["TESTING"] = testing

    # Configure static folder
    root_dir = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(root_dir, "frontend")
    app.static_folder = static_dir

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(spreadsheet_bp)

    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    return app


def main():
    """Run the application."""
    print("Starting Flask server...")
    app = create_app()

    # Get the local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Print server URLs
    urls = [
        f"http://localhost:{PORT}",
        f"http://127.0.0.1:{PORT}",
        f"http://{local_ip}:{PORT}",
    ]
    print("Server will be available at:")
    for url in urls:
        print(url)

    try:
        socketio.run(
            app,
            host=HOST,
            port=PORT,
            debug=DEBUG,
            allow_unsafe_werkzeug=True,
            use_reloader=False,  # Disable reloader to prevent duplicate sockets
        )
    except Exception as e:
        print(f"Error starting server: {e!s}")
        print("Make sure no other application is using port 5000")


if __name__ == "__main__":
    main()
