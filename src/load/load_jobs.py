#This file loads database using sqlite

import sqlite3
from typing import Any, Dict, List


def init_database(db_path: str = "data/processed/jobs.db") -> None:
    #Create the target tables and analytical indexes
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_jobs (
            job_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            date_posted TEXT NOT NULL,
            seniority TEXT NOT NULL,
            domain TEXT NOT NULL,
            skills TEXT,
            skill_count INTEGER
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_location ON dim_jobs(location);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain ON dim_jobs(domain);")

    conn.commit()
    conn.close()


def load_jobs_to_db(jobs: List[Dict[str, Any]], db_path: str = "data/processed/jobs.db") -> int:
    #Insert or replace enriched job records into SQLite
    init_database(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insert_query = """
        INSERT OR REPLACE INTO dim_jobs (
            job_id, title, company, location, date_posted, 
            seniority, domain, skills, skill_count
        ) VALUES (
            :job_id, :title, :company, :location, :date_posted, 
            :seniority, :domain, :skills, :skill_count
        )
    """

    cursor.executemany(insert_query, jobs)
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected