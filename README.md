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
   
   Note: Make sure Redis server is running and the application has started successfully. You should see the login page when accessing the URL.

#### EKS Deployment

1. **Configure AWS CLI**
   ```bash
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Enter your default region (e.g., us-west-2)
   # Enter your preferred output format (json)
   ```

2. **Create EKS Cluster**
   ```bash
   # Create cluster using the provided configuration
   eksctl create cluster -f kubernetes/eks-cluster.yaml
   
   # Verify cluster creation
   eksctl get cluster --name spreadsheet-app-cluster --region us-west-2
   ```

3. **Update kubeconfig**
   ```bash
   # Update kubeconfig to connect to your cluster
   aws eks update-kubeconfig --name spreadsheet-app-cluster --region us-west-2
   
   # Verify connection
   kubectl config current-context
   ```

4. **Deploy Application**
   ```bash
   # Create namespace
   kubectl create namespace spreadsheet-app
   
   # Deploy Redis
   kubectl apply -f kubernetes/redis.yaml
   
   # Deploy main application
   kubectl apply -f kubernetes/deployment.yaml
   
   # Deploy ingress (if needed)
   kubectl apply -f kubernetes/ingress.yaml
   ```

5. **Monitor Deployment**
   ```bash
   # Check pod status
   kubectl get pods -n spreadsheet-app
   
   # Check service status
   kubectl get svc -n spreadsheet-app
   
   # View application logs
   kubectl logs -n spreadsheet-app deployment/spreadsheet-app
   ```

6. **Access Application**
   There are multiple ways to access your application in EKS:

   a. **Using LoadBalancer (Recommended for Production)**
   ```bash
   # Get the LoadBalancer URL
   kubectl get svc spreadsheet-app-service -n spreadsheet-app -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
   ```
   The application will be available at: `http://<loadbalancer-url>`
   - This URL is publicly accessible
   - It may take a few minutes for the LoadBalancer to be fully provisioned
   - The URL remains stable unless you delete and recreate the service

   b. **Using Port Forwarding (For Development/Testing)**
   ```bash
   # Forward local port 8080 to service port 80
   kubectl port-forward -n spreadsheet-app svc/spreadsheet-app-service 8080:80
   ```
   Then access the application at: `http://localhost:8080`
   - This method is useful for local testing
   - The connection will be terminated when you stop the port-forward command
   - Only accessible from your local machine

   c. **Using Ingress (If configured)**
   ```bash
   # Get the ingress host
   kubectl get ingress -n spreadsheet-app
   ```
   Access the application using the hostname from the ingress
   - Requires proper DNS configuration
   - Supports custom domains and SSL
   - More suitable for production environments

   Note: 
   - The application might take a few minutes to be fully accessible after deployment
   - If you can't access the application, check the troubleshooting section
   - For security in production, consider setting up HTTPS and proper authentication

7. **Troubleshooting**
   - If pods are not starting, check logs: `kubectl logs -n spreadsheet-app <pod-name>`
   - If service is not accessible, verify LoadBalancer status: `kubectl describe svc spreadsheet-app-service -n spreadsheet-app`
   - For memory issues, check pod status: `kubectl describe pod -n spreadsheet-app -l app=spreadsheet-app`

8. **Scaling and Updates**
   ```bash
   # Scale the application
   kubectl scale deployment spreadsheet-app -n spreadsheet-app --replicas=3
   
   # Update the application
   kubectl set image deployment/spreadsheet-app spreadsheet-app=your-new-image:tag -n spreadsheet-app
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