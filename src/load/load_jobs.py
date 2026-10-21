import json
import sqlite3
from pathlib import Path


# Locate the project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Locate the cleaned job data and SQLite database.
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "adzuna_jobs_clean.json"
DATABASE_FILE = PROJECT_ROOT / "data" / "processed" / "jobs.db"


def read_cleaned_jobs():
    """Read cleaned job records from the JSON file."""

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
