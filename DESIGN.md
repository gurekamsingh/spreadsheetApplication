# Spreadsheet Application Design Document

## System Architecture

### Components
1. Frontend (HTML, CSS, JavaScript)
   - User interface
   - Real-time updates via Socket.IO
   - Write access management UI
   - Visual status indicators

2. Backend (Python, Flask)
   - REST API endpoints
   - Socket.IO server
   - Database operations
   - Authentication
   - Write access queue management

3. Database (DuckDB)
   - User data
   - Sales records
   - Categories

4. Session Management (Redis)
   - Write access queue
   - User sessions
   - Lock management

### Sequence Diagrams

#### Write Access Request Flow
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Redis
    participant DuckDB

    User->>Frontend: Click "Request Write Access"
    Frontend->>Backend: Socket.IO: request_write_access
    Backend->>Redis: Check current lock
    alt Lock Available
        Redis->>Backend: Grant lock
        Backend->>DuckDB: Update user status
        Backend->>Frontend: Socket.IO: access_granted
        Frontend->>User: Show write access badge
    else Lock Not Available
        Redis->>Backend: Add to queue
        Backend->>Frontend: Socket.IO: added_to_queue
        Frontend->>User: Show queue position
    end
```

#### Sales Data Update Flow
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Redis
    participant DuckDB

    User->>Frontend: Enter sale data
    Frontend->>Backend: Socket.IO: update_sale
    Backend->>Redis: Verify write access
    Redis->>Backend: Confirm access
    Backend->>DuckDB: Save sale data
    DuckDB->>Backend: Confirm save
    Backend->>Frontend: Socket.IO: update_success
    Backend->>Frontend: Socket.IO: broadcast_update
    Frontend->>User: Show success message
```

### Write Access System

#### Queue Management
- Redis-based queue system
- First-in-first-out (FIFO) queue
- Automatic timeout after 10 seconds of inactivity
- Visual status indicator in UI

#### Access Control
1. Request Process:
   - User clicks "Request Write Access"
   - System checks current lock status
   - If available, grants access immediately
   - If not available, adds to queue

2. Release Process:
   - Automatic after 10 seconds of inactivity
   - Manual release on logout
   - Next user in queue receives access
   - Broadcasts update to all clients

3. UI Indicators:
   - Green badge shows when user has write access
   - Disabled buttons when no write access
   - Success/error messages for access changes

## User Interface

### Layout
1. Header
   - Application title
   - Write access status badge
   - Action buttons (Save, Request Access, Logout)

2. Main Content
   - Sales data table
   - Add sale modal
   - Success/error alerts

### Features
1. Authentication
   - Login form
   - Signup form
   - Session management

2. Data Management
   - View sales data
   - Add new sales
   - Category selection
   - Date formatting

3. Real-time Updates
   - Automatic data refresh
   - Write access status updates
   - Queue position updates

## Database Schema

### Tables
1. Users
   ```sql
   CREATE TABLE users (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT UNIQUE NOT NULL,
       password_hash TEXT NOT NULL
   );
   ```

2. Sales
   ```sql
   CREATE TABLE sales (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       date DATE NOT NULL,
       invoice_number TEXT NOT NULL,
       customer_name TEXT NOT NULL,
       location TEXT NOT NULL,
       product_name TEXT NOT NULL,
       category TEXT NOT NULL,
       volume_sold REAL NOT NULL,
       unit TEXT NOT NULL,
       created_by TEXT NOT NULL
   );
   ```

3. Categories
   ```sql
   CREATE TABLE categories (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL UNIQUE,
       description TEXT
   );
   ```

## Security Measures

1. Authentication
   - Password hashing
   - Session management
   - CSRF protection

2. Data Access
   - Write access control
   - Input validation
   - SQL injection prevention

3. Real-time Features
   - Socket.IO authentication
   - Message validation
   - Error handling

## Error Handling

1. Frontend
   - User-friendly error messages
   - Automatic retry for failed operations
   - Connection status monitoring

2. Backend
   - Input validation
   - Database error handling
   - Socket.IO error handling

## Future Enhancements

1. Features
   - Data export
   - Advanced filtering
   - User roles
   - Data backup
   - Visualization

2. Performance
   - Caching
   - Pagination
   - Optimized queries

3. Security
   - Rate limiting
   - Audit logging
   - Enhanced validation

## Project Structure
```
spreadsheetApplication/
├── backend/
│   ├── routes/
│   │   └── spreadsheet.py
│   └── app.py
├── frontend/
│   └── spreadsheet.html
├── database/
│   └── sales.db
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── certs/
│   ├── server.crt
│   └── server.key
├── README.md
├── DESIGN.md
├── run.py
└── setup.py
``` 
