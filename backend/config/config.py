"""Configuration settings for the application."""

import os

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
print(f"Project root directory: {PROJECT_ROOT}")

# Flask settings
SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
PORT = int(os.environ.get("FLASK_PORT", "5000"))

# Static files
STATIC_FOLDER = os.path.join(PROJECT_ROOT, "frontend")
print(f"Static folder path: {STATIC_FOLDER}")
print(f"Static folder exists: {os.path.exists(STATIC_FOLDER)}")
if os.path.exists(STATIC_FOLDER):
    print(f"Contents of static folder: {os.listdir(STATIC_FOLDER)}")

# Database settings
DB_DIR = os.path.join(PROJECT_ROOT, "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "spreadsheet.db")

# Redis settings
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_DB = int(os.environ.get("REDIS_DB", "0"))
REDIS_TIMEOUT = int(os.environ.get("REDIS_TIMEOUT", "5"))

# Redis Keys
LOCK_KEY = "spreadsheet_lock"
ACTIVE_USERS_KEY = "active_users"
WRITE_QUEUE_KEY = "write_queue"

# Application Settings
DEBUG = True
HOST = "0.0.0.0"
PORT = 5000
