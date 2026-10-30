import sqlite3
from pathlib import Path

database_path = Path("data/processed/jobs_recovered.db")

if not database_path.exists():
    print("Recovery database was not found.")
else:
    connection = sqlite3.connect(database_path)

    try:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()

        print("Tables:", [table[0] for table in tables])

        job_count = connection.execute(
            "SELECT COUNT(*) FROM adzuna_jobs"
        ).fetchone()[0]

        print("Recovered job records:", job_count)

        integrity = connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        print("Integrity check:", integrity)

    finally:
        connection.close()
