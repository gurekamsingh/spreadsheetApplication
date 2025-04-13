"""Setup script for the spreadsheet application."""

from setuptools import find_packages, setup

setup(
    name="spreadsheet-application",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["*.db", "*.sql"],
    },
    install_requires=[
        "flask>=3.0.0",
        "flask-socketio>=5.0.0",
        "python-dotenv>=1.0.0",
        "redis>=5.0.0",
        "duckdb>=0.9.0",
        "werkzeug>=3.0.0",
        "python-socketio>=5.0.0",
        "eventlet>=0.33.0",
    ],
    extras_require={
        "dev": [
            "ruff>=0.3.0",
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
        ],
    },
)
