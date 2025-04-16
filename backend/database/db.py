"""Database connection and schema management."""

import duckdb

from backend.config.config import DB_PATH


def get_db():
    """Get database connection."""
    db = duckdb.connect(DB_PATH)
    init_schema(db)
    return db


def init_schema(db):
    """Initialize database schema."""
    # Create users table
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            username VARCHAR NOT NULL UNIQUE,
            password_hash VARCHAR NOT NULL,
            email VARCHAR NOT NULL UNIQUE,
            name VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Create categories table
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id BIGINT PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            description VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Create sales table
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id BIGINT PRIMARY KEY,
            date DATE NOT NULL,
            invoice_number VARCHAR NOT NULL UNIQUE,
            customer_name VARCHAR NOT NULL,
            location VARCHAR NOT NULL,
            product_name VARCHAR NOT NULL,
            category VARCHAR NOT NULL,
            volume_sold DECIMAL(10,2) NOT NULL,
            unit VARCHAR NOT NULL,
            created_by VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Insert default categories if they don't exist
    default_categories = [
        (1, "Soft Drinks", "Carbonated soft drinks and colas"),
        (2, "Soda", "Soda water and carbonated beverages"),
        (3, "Coffee", "Coffee and coffee-based beverages"),
        (4, "Beverages", "General beverages"),
        (5, "Beer", "Beer and alcoholic beverages"),
        (6, "Creamers", "Coffee creamers and dairy alternatives"),
        (7, "Mineral Water", "Mineral and spring water"),
        (8, "Juice", "Fruit juices and juice drinks"),
        (9, "Tea", "Bottled and canned tea"),
        (10, "Milk", "Dairy milk and milk-based drinks"),
        (11, "Dairy", "Other dairy products like yogurt drinks and kefir"),
        (12, "Energy Drinks", "Energy and sports drinks"),
        (13, "Other", "Other types of beverages"),
    ]

    for category in default_categories:
        db.execute(
            """
            INSERT OR IGNORE INTO categories (id, name, description)
            VALUES (?, ?, ?)
            """,
            category,
        )
