import sqlite3
from pathlib import Path

DATABASE_FILE = Path("data/processed/jobs.db")

print("Database exists:", DATABASE_FILE.exists())

connection = sqlite3.connect(DATABASE_FILE)

tables = connection.execute(
    "SELECT name FROM sqlite_master "
    "WHERE type='table' ORDER BY name"
).fetchall()

print("Tables:", tables)

sample_count = connection.execute(
    "SELECT COUNT(*) FROM dim_jobs"
).fetchone()[0]

adzuna_count = connection.execute(
    "SELECT COUNT(*) FROM adzuna_jobs"
).fetchone()[0]

unique_ids = connection.execute(
    "SELECT COUNT(DISTINCT adzuna_id) FROM adzuna_jobs"
).fetchone()[0]

missing_ids = connection.execute(
    "SELECT COUNT(*) FROM adzuna_jobs "
    "WHERE adzuna_id IS NULL OR adzuna_id = ''"
).fetchone()[0]

print("Original sample records:", sample_count)
print("Adzuna records:", adzuna_count)
print("Unique Adzuna IDs:", unique_ids)
print("Missing Adzuna IDs:", missing_ids)

connection.close()