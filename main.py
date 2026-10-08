#This file is the pipeline entry point

import sys
from pathlib import Path

#Add project root to sys.path so modules import reliably
sys.path.append(str(Path(__file__).resolve().parent))

from src.extract.extract_jobs import extract_jobs
from src.transform.transform_jobs import transform_jobs
from src.load.load_jobs import load_jobs_to_db


def main():
    raw_path = "data/raw/jobs.csv"
    db_path = "data/processed/jobs.db"

    print("==========================================")
    print("  SA Tech Job Market Data Pipeline (ETL)  ")
    print("==========================================")

    # 1. Extract
    print(f"[1/3] Extracting raw data from: {raw_path}")
    raw_jobs = extract_jobs(raw_path)
    print(f"      Extracted {len(raw_jobs)} records.")

    # 2. Transform
    print("[2/3] Transforming and enriching records...")
    transformed_jobs = transform_jobs(raw_jobs)
    print(f"      Enriched {len(transformed_jobs)} records.")

    # 3. Load
    print(f"[3/3] Loading into SQLite database: {db_path}")
    loaded_count = load_jobs_to_db(transformed_jobs, db_path)
    print(f"      Success! {loaded_count} rows loaded into dim_jobs.")
    print("==========================================")


if __name__ == "__main__":
    main()