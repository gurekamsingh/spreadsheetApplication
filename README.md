# Spreadsheet Application

A real-time collaborative spreadsheet application for tracking sales data.

## Features

- User authentication (login/signup)
- Real-time data updates using Socket.IO
- Write access management with queue system
- Visual write access status indicator
- Sales data management (add, view)
- Category management
- Responsive design

## Write Access System

The application implements a write access system to prevent concurrent edits:

1. Users can request write access
2. If no one has write access, it's granted immediately
3. If someone else has write access, the user is added to a queue
4. Write access is automatically released after 10 seconds of inactivity
5. When write access is released, it's granted to the next user in the queue
6. Users can only edit their own entries
7. A visual indicator shows when a user has write access

## Technologies Used

- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Backend: Python, Flask, Socket.IO
- Database: DuckDB
- Authentication: Session-based
- Real-time updates: Socket.IO

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:
   ```bash
   python app.py
   ```

3. Access the application at `http://localhost:5000`

## Project Structure

```
spreadsheetApplication/
├── backend/
│   ├── app.py
│   ├── database/
│   │   ├── schema.sql
│   │   └── spreadsheet.db
│   └── routes/
│       ├── auth.py
│       └── spreadsheet.py
├── frontend/
│   ├── index.html
│   ├── signup.html
│   └── spreadsheet.html
└── requirements.txt
```

## Security Features

- Session-based authentication
- Write access control
- Input validation
- SQL injection prevention
- XSS protection

## Future Improvements

- Add data export functionality
- Implement data filtering and sorting
- Add user roles and permissions
- Implement data backup system
- Add data visualization features

## Prerequisites

- Python 3.8 or higher
- Redis server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/spreadsheetApplication.git
cd spreadsheetApplication
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies using uv:
```bash
uv pip install -e .
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

## API Endpoints

### Authentication
- `POST /signup` - Register a new user
- `POST /login`