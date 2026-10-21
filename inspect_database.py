
import sqlite3
from pathlib import Path

# Locate the existing database.
database_path = Path("data/processed/jobs.db")

print("Database exists:", database_path.exists())

if database_path.exists():
    # Open the database without changing its contents.
    connection = sqlite3.connect(database_path)

    try:
        query = """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
        """

        tables = connection.execute(query).fetchall()
        print("Tables:", tables)

        # Inspect the columns in each table.
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")

            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()

            for column in columns:
                print(column)

    finally:
        connection.close()
