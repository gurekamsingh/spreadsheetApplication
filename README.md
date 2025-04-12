# Spreadsheet Application

A real-time collaborative spreadsheet application for tracking sales data with write access control and real-time updates.

## Features

- User authentication (login/signup)
- Real-time data updates using Socket.IO
- Write access management with queue system
- Visual write access status indicator
- Sales data management (add, view)
- Category management
- Responsive design

## Technologies Used

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5 for responsive design
- Socket.IO client for real-time updates

### Backend
- Python 3.8+
- Flask 3.0+ (Web framework)
- Flask-SocketIO 5.3+ (Real-time communication)
- DuckDB 0.10+ (Database)
- Redis 5.0+ (Write access management)
- Python-dotenv 1.0+ (Environment management)
- Werkzeug 3.0+ (WSGI utilities)

### Development Tools
- UV (Package manager)
- Ruff (Linting and formatting)
- Pre-commit (Git hooks)

## Prerequisites

- Python 3.8 or higher
- Redis server
- Git
- UV package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/spreadsheetApplication.git
cd spreadsheetApplication
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies using UV:
```bash
uv pip install -e .
```

4. Set up environment variables:
```bash
# Create a .env file in the project root
FLASK_APP=backend.app
FLASK_ENV=development
SECRET_KEY=your-secret-key
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Project Structure

```
spreadsheetApplication/
├── backend/
│   ├── config/
│   │   └── config.py         # Configuration settings
│   ├── database/
│   │   ├── db.py            # Database initialization and connection
│   │   ├── redis_client.py  # Redis client functions
│   │   └── schema.sql       # Database schema
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   └── spreadsheet.py   # Spreadsheet operations routes
│   ├── utils/               # Utility functions
│   ├── test/                # Test files
│   ├── extensions.py        # Flask extensions (SocketIO)
│   ├── __init__.py         # Package initialization
│   └── app.py              # Main Flask application
├── frontend/
│   ├── index.html          # Login page
│   ├── signup.html         # Signup page
│   └── spreadsheet.html    # Main spreadsheet interface
├── database/
│   └── spreadsheet.db      # DuckDB database file
├── kubernetes/             # Kubernetes deployment files
├── certs/                  # SSL certificates
├── .github/                # GitHub Actions workflows
├── .ruff_cache/           # Ruff cache directory
├── venv/                  # Virtual environment
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── Dockerfile            # Docker build configuration
├── .dockerignore        # Docker ignore rules
├── generate_cert.py     # Certificate generation script
├── LICENSE              # Project license
├── pyproject.toml      # Project configuration
├── run.py              # Application entry point
├── setup.py            # Package installation script
├── view_tables.py      # Database table viewer script
└── README.md           # Project documentation
```

## Running the Application

1. Start Redis server:
```bash
# Windows
redis-server

# Linux/Mac
sudo service redis-server start
```

2. Start the Flask application:
```bash
python -m backend.app
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Development Guidelines

### Code Quality

This project uses Ruff for linting and code formatting. Configuration is in `pyproject.toml`.

```bash
# Check for linting issues
ruff check .

# Automatically fix linting issues
ruff check --fix .

# Format code
ruff format .
```

### Pre-commit Hooks

Pre-commit hooks ensure code quality before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Write Access System

The application implements a write access system to prevent concurrent edits:

1. Users can request write access
2. If no one has write access, it's granted immediately
3. If someone else has write access, the user is added to a queue
4. Write access is automatically released after 10 seconds of inactivity
5. When write access is released, it's granted to the next user in the queue
6. A visual indicator shows when a user has write access

## Security Features

- Session-based authentication
- Write access control
- Input validation
- SQL injection prevention
- XSS protection
- CSRF protection

## API Endpoints

### Authentication
- `POST /signup` - Register a new user
- `POST /login` - User login

### Spreadsheet Operations
- `GET /read_data` - Read sales data with queue status
- `POST /write` - Write new sales data
- `Socket.IO /request_write_access` - Request write access
- `Socket.IO /release_write_access` - Release write access

## Future Improvements

- Data export functionality
- Data filtering and sorting
- User roles and permissions
- Data backup system
- Data visualization features