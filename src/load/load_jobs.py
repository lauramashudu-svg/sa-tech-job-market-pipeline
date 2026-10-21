import json
import sqlite3
from pathlib import Path


#Locate the project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#Locate the cleaned job data and SQLite database.
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "adzuna_jobs_clean.json"
DATABASE_FILE = PROJECT_ROOT / "data" / "processed" / "jobs.db"


def read_cleaned_jobs():
    #Read cleaned job records from the JSON file

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned jobs file was not found: {DATA_FILE}"
        )

    with DATA_FILE.open("r", encoding="utf-8") as file:
        jobs = json.load(file)

    if not isinstance(jobs, list):
        raise ValueError("The cleaned jobs file must contain a list.")

    print(f"Read {len(jobs)} cleaned job records.")

    return jobs


def load_jobs(jobs):
    #Load cleaned jobs into the existing SQLite database.

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        #Start a transaction so changes can be rolled back on error.
        cursor = connection.cursor()

        #Store Adzuna's original ID to prevent duplicate imports.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adzuna_jobs (
                adzuna_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                category TEXT,
                date_posted TEXT,
                salary_min REAL,
                salary_max REAL,
                salary_is_predicted TEXT,
                job_url TEXT,
                description TEXT
            )
        """)

        inserted = 0
        duplicates_skipped = 0

        for job in jobs:
            #Skip records without a usable ID or title.
            if not job.get("job_id") or not job.get("job_title"):
                print("Skipping a job with missing ID or title")
                continue

            cursor.execute("""
                INSERT OR IGNORE INTO adzuna_jobs (
                    adzuna_id,
                    title,
                    company,
                    location,
                    category,
                    date_posted,
                    salary_min,
                    salary_max,
                    salary_is_predicted,
                    job_url,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(job["job_id"]),
                job.get("job_title"),
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

            if cursor.rowcount == 1:
                inserted += 1
            else:
                duplicates_skipped += 1
        
        connection.commit()
        print(f"New Adzuna jobs inserted: {inserted}")
        print(f"Duplicate jobs skipped: {duplicates_skipped}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
