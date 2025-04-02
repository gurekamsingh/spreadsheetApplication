# Technical Design Document

## Architecture Overview

The Spreadsheet Application follows a modern client-server architecture with clear separation of concerns and modular design. The system is built using a stack of proven technologies that work together to provide a robust, scalable, and maintainable solution.

### System Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Client Layer   │     │  Server Layer   │     │  Data Layer     │
│  (Browser)      │     │  (Flask)        │     │  (DuckDB)       │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │                       │                       │
         │                       │                       │
┌────────▼────────┐     ┌────────▼────────┐     ┌────────▼────────┐
│                 │     │                 │     │                 │
│  Socket.IO      │     │  Redis Cache    │     │  File System    │
│  (WebSocket)    │     │  (Real-time)    │     │  (Storage)      │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Component Details

#### 1. Client Layer (Frontend)
- **Technology Stack**:
  - HTML5 for structure
  - CSS3 with Bootstrap for responsive design
  - JavaScript (ES6+) for client-side logic
  - Socket.IO client for real-time communication

- **Key Features**:
  - Responsive single-page application
  - Real-time data updates
  - Write access queue management
  - Form validation and error handling
  - Session management

#### 2. Server Layer (Backend)
- **Core Framework**:
  - Flask web framework
  - Blueprint-based route organization
  - RESTful API design
  - Session-based authentication

- **Key Components**:
  - Authentication Blueprint (`auth_bp`)
  - Spreadsheet Blueprint (`spreadsheet_bp`)
  - Socket.IO integration
  - Request validation middleware
  - Error handling middleware

#### 3. Real-time Layer
- **Redis Implementation**:
  - Write access management
  - User session tracking
  - Queue system
  - Real-time data synchronization

- **Socket.IO Features**:
  - Bi-directional communication
  - Event-based updates
  - Automatic reconnection
  - Room-based broadcasting

#### 4. Data Layer
- **DuckDB Implementation**:
  - SQL-based data operations
  - Transaction support
  - Foreign key constraints
  - Index optimization

- **Data Management**:
  - Connection pooling
  - Query optimization
  - Transaction isolation
  - Data integrity checks

### Data Flow

1. **User Authentication Flow**:
   ```
   Client -> Flask Server -> DuckDB -> Session Management
   ```

2. **Data Read Flow**:
   ```
   Client -> Flask Server -> DuckDB -> Response
   ```

3. **Data Write Flow**:
   ```
   Client -> Redis (Write Access Check) -> Flask Server -> DuckDB -> Socket.IO Broadcast
   ```

4. **Real-time Update Flow**:
   ```
   Server -> Socket.IO -> All Connected Clients
   ```

### Security Architecture

1. **Authentication Layer**:
   - Session-based authentication
   - Password hashing with salt
   - CSRF protection
   - Secure cookie handling

2. **Authorization Layer**:
   - Write access control
   - Resource-based permissions
   - Session validation
   - Request validation

3. **Data Security**:
   - SQL injection prevention
   - XSS protection
   - Input sanitization
   - Output encoding

### Scalability Considerations

1. **Horizontal Scaling**:
   - Stateless server design
   - Redis for session management
   - Load balancer ready
   - Database connection pooling

2. **Vertical Scaling**:
   - Query optimization
   - Caching strategies
   - Resource monitoring
   - Performance tuning

3. **High Availability**:
   - Redis cluster support
   - Database replication
   - Failover mechanisms
   - Backup strategies

### Deployment Architecture

1. **Development Environment**:
   - Local development setup
   - Debug mode enabled
   - Detailed logging
   - Hot reloading

2. **Production Environment**:
   - Production-grade server
   - SSL/TLS encryption
   - Rate limiting
   - Monitoring and alerting

3. **Container Support**:
   - Docker compatibility
   - Environment isolation
   - Resource management
   - Easy deployment

## Database Design

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL
)
```

### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description VARCHAR
)
```

### Sales Table
```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    invoice_number VARCHAR NOT NULL,
    customer_name VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    product_name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    volume_sold DECIMAL(10,2) NOT NULL,
    unit VARCHAR NOT NULL,
    created_by VARCHAR NOT NULL,
    FOREIGN KEY (category) REFERENCES categories(name)
)
```

## Write Access System Design

### Redis Keys
- `write_lock`: Stores the username of the user with current write access
- `write_queue`: List of usernames waiting for write access
- `active_users`: Set of currently active users

### Write Access Flow
1. User requests write access
2. System checks if any user has write access
3. If no user has access:
   - Grant access to requesting user
   - Set 10-second expiration on lock
4. If another user has access:
   - Add requesting user to queue
   - Return queue position

### Lock Expiration
- Write access locks expire after 10 seconds of inactivity
- Users must request access again after expiration
- Queue position is maintained until access is granted

## Real-time Updates

### Socket.IO Events
- `data_updated`: Broadcasted when data changes
- `write_access_granted`: Notifies user of write access
- `write_access_released`: Notifies users when write access is released

### Update Flow
1. User makes changes
2. Server updates database
3. Server broadcasts update via Socket.IO
4. All connected clients receive update

## Security Design

### Authentication
- Session-based authentication
- Password hashing using Werkzeug's security functions
- Session timeout after 30 minutes of inactivity

### Data Validation
- Input validation on both client and server
- SQL injection prevention through parameterized queries
- XSS prevention through proper escaping

### Write Access Security
- Server-side validation of write access
- Redis-based locking mechanism
- Automatic lock expiration

## Error Handling

### Database Errors
- Transaction rollback on errors
- Connection retry mechanism
- Graceful degradation when database is unavailable

### Redis Errors
- Fallback to read-only mode
- Queue system degradation
- User notification of service issues

### Network Errors
- Socket.IO reconnection handling
- API request retry mechanism
- User-friendly error messages

## Performance Considerations

### Database Optimization
- Indexed columns for frequent queries
- Efficient JOIN operations
- Transaction management

### Redis Optimization
- Key expiration for automatic cleanup
- Efficient queue operations
- Minimal data storage

### Frontend Optimization
- Lazy loading of data
- Efficient DOM updates
- Minimal network requests

## Scalability Design

### Horizontal Scaling
- Stateless server design
- Redis for session management
- Database connection pooling

### Load Balancing
- Multiple server instances possible
- Redis cluster support
- Database replication ready

## Monitoring and Logging

### Server Logs
- Request/response logging
- Error tracking
- Performance metrics

### Database Logs
- Query performance
- Connection issues
- Transaction failures

### Redis Logs
- Connection status
- Queue operations
- Lock management

## Future Enhancements

### Planned Features
1. User roles and permissions
2. Data export/import
3. Advanced filtering and search
4. Data visualization
5. API rate limiting

### Technical Improvements
1. Database query optimization
2. Caching layer
3. Automated testing
4. CI/CD pipeline
5. Containerization support

## Development Guidelines

### Code Style
- PEP 8 compliance
- Type hints
- Docstring documentation
- Modular design

### Testing
- Unit tests for core functionality
- Integration tests for API endpoints
- End-to-end testing
- Performance testing

### Deployment
- Environment configuration
- Database migrations
- Backup procedures
- Monitoring setup 