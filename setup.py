from setuptools import find_packages, setup

setup(
    name="spreadsheet-application",
    version="0.1",
    packages=find_packages(include=["backend*"]),
    install_requires=[
        "flask",
        "flask-socketio",
        "duckdb",
        "redis",
        "werkzeug",
        "python-socketio",
        "eventlet",
    ],
    python_requires=">=3.7",
)
