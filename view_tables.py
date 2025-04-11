import os

import duckdb
from tabulate import tabulate


def view_tables():
    # Connect to the database
    db_path = os.path.join("database", "spreadsheet.db")
    conn = duckdb.connect(db_path)

    # Get all tables
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    print("\nAvailable tables:")
    for table in tables:
        print(f"\nTable: {table[0]}")

        # Get table schema
        schema = conn.execute(f"DESCRIBE {table[0]}").fetchall()
        print("\nSchema:")
        headers = ["Column", "Type"]
        print(tabulate(schema, headers=headers, tablefmt="grid"))

        # Get sample data
        print("\nSample data (first 5 rows):")
        data = conn.execute(f"SELECT * FROM {table[0]} LIMIT 5").fetchall()
        if data:
            # Get column names
            columns = conn.execute(f"SELECT * FROM {table[0]} LIMIT 1").description
            headers = [col[0] for col in columns]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print("No data in table")


if __name__ == "__main__":
    view_tables()
