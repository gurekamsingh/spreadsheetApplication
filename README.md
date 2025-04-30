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

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Amazon EKS (Elastic Kubernetes Service)
- **CI/CD**: AWS CodePipeline
- **Monitoring**: AWS CloudWatch

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Redis server
- Git
- UV Package Manager
- AWS CLI configured with appropriate credentials
- kubectl configured for EKS cluster
- eksctl for cluster management

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
   Create a `.env` file in the root directory with:
   ```bash
   FLASK_APP=backend.app
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

### Running the Application

#### Local Development

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

#### EKS Deployment

1. **Configure AWS CLI**
   ```bash
   aws configure
   ```

2. **Create EKS Cluster**
   ```bash
   eksctl create cluster --name spreadsheet-app --region your-region --nodegroup-name standard-workers --node-type t3.medium --nodes 3 --nodes-min 1 --nodes-max 4 --managed
   ```

3. **Deploy Application**
   ```bash
   kubectl apply -f kubernetes/
   ```

4. **Access Application**
   ```bash
   kubectl get svc spreadsheet-app-service
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
├── kubernetes/           # EKS deployment configurations
├── tests/                # Test suite
├── database/            # Local database storage
└── docs/               # Documentation
```

## Database Management

The application uses DuckDB for data storage with the following features:
- File-based storage for local development
- EKS persistent volume for production
- Automatic schema management
- Real-time data synchronization

## Contributing

We welcome contributions! Please follow these steps:

1. Create a feature branch (`git checkout -b feature/feature-name`)
2. Commit your changes (`git commit -m 'Add feature description'`)
3. Push to the branch (`git push origin feature/feature-name`)
4. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact the maintainers through the project's communication channels.