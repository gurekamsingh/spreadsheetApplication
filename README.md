# Spreadsheet Application

A real-time collaborative spreadsheet application built with Flask, DuckDB, and Redis. This application allows multiple users to view sales data while ensuring only one user can edit at a time through a write access queue system.

## Features

- User Authentication (Signup/Login)
- Real-time data updates using Socket.IO
- Write access queue system for data consistency
- Sales data management with categories
- Responsive web interface
- Data persistence using DuckDB
- Redis for managing write access and real-time features

## Prerequisites

- Python 3.8 or higher
- Redis server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd spreadsheetApplication
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Start Redis server:
```bash
# On Windows (if using WSL or Windows Subsystem for Linux)
redis-server
# On Unix or MacOS
redis-server
```

## Project Structure

```
spreadsheetApplication/
├── backend/
│   ├── config/
│   │   └── config.py         # Configuration settings
│   ├── database/
│   │   ├── db.py            # Database initialization and connection
│   │   └── redis_client.py  # Redis client functions
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   └── spreadsheet.py   # Spreadsheet operations routes
│   ├── extensions.py        # Flask extensions (SocketIO)
│   └── app.py              # Main Flask application
├── frontend/
│   ├── index.html          # Login page
│   ├── signup.html         # Signup page
│   └── spreadsheet.html    # Main spreadsheet interface
├── database/
│   └── spreadsheet.db      # DuckDB database file
├── requirements.txt        # Python dependencies
└── run.py                 # Application entry point
```

## Running the Application

1. Start the Flask application:
```bash
python run.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Database Management

To view the database tables and their contents, you can use the provided script:

```bash
python view_tables.py
```

This will display:
- Available tables
- Table schemas
- Sample data (first 5 rows) from each table

## Write Access System

The application implements a write access queue system to ensure data consistency:

1. Only one user can have write access at a time
2. Users must request write access to make changes
3. Write access is automatically released after 10 seconds of inactivity
4. Other users are queued for write access

## API Endpoints

### Authentication
- `POST /signup` - Register a new user
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /check_auth` - Check authentication status

### Spreadsheet Operations
- `GET /read` - Read sales data
- `POST /write` - Write new sale data
- `POST /request_write_access` - Request write access
- `POST /release_write_access` - Release write access

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask web framework
- DuckDB for data storage
- Redis for real-time features
- Socket.IO for real-time communication
- Bootstrap for the UI components