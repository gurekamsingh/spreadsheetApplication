from setuptools import find_packages, setup

setup(
    name="spreadsheet-application",
    version="0.1",
    packages=find_packages(include=["backend*"]),
    install_requires=[
        "flask>=2.0.0",
        "flask-socketio>=5.0.0",
        "duckdb>=0.9.0",
        "redis>=4.0.0",
        "werkzeug>=2.0.0",
        "python-socketio>=5.0.0",
        "eventlet>=0.33.0",
        "ruff>=0.3.0",
        "pytest>=8.0.0",
    ],
    python_requires=">=3.7",
)
