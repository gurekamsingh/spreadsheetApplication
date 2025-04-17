# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir \
    flask==3.0.2 \
    flask-socketio==5.3.6 \
    python-socketio==5.11.1 \
    redis==5.0.1 \
    python-dotenv==1.0.1 \
    sqlalchemy==2.0.27 \
    psycopg2-binary==2.9.9 \
    flask-login==0.6.3 \
    werkzeug==3.0.1 \
    eventlet==0.35.2 \
    duckdb==0.10.0

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Start the application
CMD ["python", "backend/app.py"] 