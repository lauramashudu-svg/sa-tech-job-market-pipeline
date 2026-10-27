
import json
import sqlite3
from pathlib import Path

# Paths to the saved data and the new recovery database
raw_path = Path("data/raw/adzuna_jobs.json")
clean_path = Path("data/processed/adzuna_jobs_clean.json")
database_path = Path("data/processed/jobs_recovered.db")

# Load the saved job records
raw_data = json.loads(raw_path.read_text(encoding="utf-8"))
clean_jobs = json.loads(clean_path.read_text(encoding="utf-8"))

raw_jobs = raw_data.get("results", [])

# Create a new database, not the damaged one
if database_path.exists():
    raise FileExistsError(
        f"{database_path} already exists. "
        "Rename it or choose another filename before continuing."
    )

connection = sqlite3.connect(database_path)

try:
    connection.execute("""
        CREATE TABLE adzuna_jobs (
            adzuna_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT,
            location TEXT,
            category TEXT,
            date_posted TEXT,
            salary_min REAL,
            salary_max REAL,
            salary_is_predicted INTEGER,
            job_url TEXT,
            description TEXT
        )
    """)

    # Load the cleaned records
    for job in clean_jobs:
        job_id = job.get("job_id")
        title = job.get("job_title")

        if not job_id or not title:
            continue

        connection.execute("""
            INSERT OR IGNORE INTO adzuna_jobs (
                adzuna_id, title, company, location, category,
                date_posted, salary_min, salary_max,
                salary_is_predicted, job_url, description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(job_id),
            title,
            job.get("company_name"),
            job.get("location"),
            job.get("category"),
            job.get("date_posted"),
            job.get("salary_min"),
            job.get("salary_max"),
            job.get("salary_is_predicted"),
            job.get("job_url"),
            job.get("description"),
        ))

    connection.commit()

    # Check the new database
    count = connection.execute(
        "SELECT COUNT(*) FROM adzuna_jobs"
    ).fetchone()[0]

    integrity = connection.execute(
        "PRAGMA integrity_check"
    ).fetchone()[0]

    print("Recovery database created:", database_path)
    print("Cleaned records available:", len(clean_jobs))
    print("Raw records available:", len(raw_jobs))
    print("Records inserted:", count)
    print("Integrity check:", integrity)

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()
