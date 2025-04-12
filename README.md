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

## Development

### Code Quality

This project uses Ruff for linting and code formatting. To run the linter:

```bash
# Check for linting issues
ruff check .

# Automatically fix linting issues
ruff check --fix .

# Format code
ruff format .
```

### Pre-commit Hooks

To ensure code quality before each commit, install pre-commit hooks:

```bash
pre-commit install
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

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

1. **Testing**
   - Runs on Python 3.8, 3.9, and 3.10
   - Checks code style with Ruff
   - Runs automated tests
   - Validates code formatting

2. **Building**
   - Creates Docker image
   - Tags with commit SHA and latest
   - Pushes to Docker Hub

3. **Deployment**
   - Deploys to Kubernetes cluster
   - Updates deployment with new image
   - Applies Kubernetes configurations

### Required Secrets

The following secrets need to be configured in your GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token
- `KUBE_CONFIG`: Your Kubernetes configuration file

## Local Development with Minikube

### Prerequisites
- Docker
- Minikube
- kubectl

### Setting up Minikube

1. Install Minikube:
   - Windows: `choco install minikube`
   - macOS: `brew install minikube`
   - Linux: Follow instructions at [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/)

2. Start Minikube:
```bash
minikube start --driver=docker --cpus=2 --memory=4g --disk-size=20g
```

3. Enable required addons:
```bash
minikube addons enable ingress
minikube addons enable metrics-server
```

4. Create namespace:
```bash
kubectl create namespace spreadsheet-app
```

### Local Development Workflow

1. Build and push Docker image:
```bash
# Build the image
docker build -t spreadsheet-app:latest .

# Load the image into Minikube
minikube image load spreadsheet-app:latest
```

2. Deploy to Minikube:
```bash
# Apply Kubernetes configurations
kubectl apply -f kubernetes/ -n spreadsheet-app

# Watch the deployment
kubectl get pods -n spreadsheet-app -w
```

3. Access the application:
```bash
# Get the service URL
minikube service spreadsheet-app -n spreadsheet-app --url
```

### Development Tips

1. To view logs:
```bash
kubectl logs -f deployment/spreadsheet-app -n spreadsheet-app
```

2. To delete and redeploy:
```bash
kubectl delete -f kubernetes/ -n spreadsheet-app
kubectl apply -f kubernetes/ -n spreadsheet-app
```

3. To stop Minikube:
```bash
minikube stop
```

4. To delete Minikube cluster:
```bash
minikube delete
```