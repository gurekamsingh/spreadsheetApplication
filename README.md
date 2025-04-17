# Spreadsheet Application

A real-time collaborative spreadsheet application for tracking sales data with write access control and real-time updates.

## Overview

The Spreadsheet Application is a modern web-based solution for managing sales data with real-time collaboration features. It provides a secure, efficient, and user-friendly interface for teams to track and manage sales records while preventing concurrent write conflicts.

## Key Features

- **Real-time Collaboration**
  - Live updates using Socket.IO
  - Write access management with queue system
  - Visual write access status indicators
  - Concurrent user support

- **Data Management**
  - Sales data tracking and management
  - Category-based organization
  - Data persistence with DuckDB
  - Real-time data synchronization

- **Security & Access Control**
  - User authentication system
  - Write access queue management
  - Session-based access control
  - Secure data transmission

- **Deployment Options**
  - Local development setup
  - Docker containerization
  - Kubernetes deployment
  - CI/CD pipeline integration

## Technology Stack

### Frontend
- **Core**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Real-time Communication**: Socket.IO Client
- **Build Tools**: UV Package Manager

### Backend
- **Framework**: Flask 3.0+
- **Database**: DuckDB 0.10+
- **Caching**: Redis 5.0+
- **Real-time**: Flask-SocketIO 5.3+
- **Security**: Werkzeug 3.0+

### Development & Deployment
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube)
- **CI/CD**: GitHub Actions
- **Code Quality**: Ruff, Pre-commit
- **Environment**: Python 3.8+

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Redis server
- Git
- Docker (optional)
- Minikube (optional)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/spreadsheetApplication.git
   cd spreadsheetApplication
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   uv pip install -e .
   ```

4. **Configure Environment**
   Create a `.env` file with:
   ```bash
   FLASK_APP=backend.app
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

## Deployment Options

### Local Development

1. **Start Redis Server**
   ```bash
   # Windows
   redis-server

   # Linux/Mac
   sudo service redis-server start
   ```

2. **Run Application**
   ```bash
   python run.py
   ```

3. **Access Application**
   Open http://localhost:5000 in your browser

### Docker Deployment

1. **Build Image**
   ```bash
   docker build -t spreadsheet-app .
   ```

2. **Run Container**
   ```bash
   docker run -p 5000:5000 spreadsheet-app
   ```

### Kubernetes Deployment

1. **Start Minikube**
   ```bash
   minikube start
   ```

2. **Deploy Application**
   ```bash
   kubectl apply -f kubernetes/
   ```

3. **Access Application**
   ```bash
   minikube service spreadsheet-app-service
   ```

## Project Structure

```
spreadsheetApplication/
├── backend/
│   ├── config/              # Configuration management
│   ├── database/           # Database operations
│   ├── routes/             # API endpoints
│   ├── utils/              # Utility functions
│   └── app.py             # Main application
├── frontend/              # User interface
├── kubernetes/           # Deployment configurations
├── tests/               # Test suite
├── database/           # Local database storage
├── certs/             # SSL certificates
├── .github/          # CI/CD workflows
└── docs/            # Documentation
```

## Database Management

The application uses DuckDB for data storage with the following features:
- Local development: File-based storage
- Production: Kubernetes persistent volume
- Automatic schema management
- Real-time data synchronization

## CI/CD Pipeline

The application uses GitHub Actions for continuous integration and deployment:

1. **Testing Phase**
   - Code linting and formatting
   - Unit and integration tests
   - Security scanning

2. **Build Phase**
   - Docker image creation
   - Image scanning
   - Push to Docker Hub

3. **Deployment Phase**
   - Kubernetes deployment
   - Health checks
   - Rollback capabilities

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [documentation](docs/)
2. Open an issue on GitHub
3. Contact the maintainers

## Acknowledgments

- Flask team for the web framework
- Socket.IO for real-time capabilities
- DuckDB for efficient data storage
- Redis for session management