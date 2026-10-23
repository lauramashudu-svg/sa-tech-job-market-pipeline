#Run the South African technology job market data pipeline.

import json

from src.extract.adzuna_api import extract_adzuna_jobs
from src.transform.transform_jobs import transform_jobs, OUTPUT_FILE
from src.load.load_jobs import load_jobs


def main():
    #Extract, transform, and load job listings.

    print("\n=== South African Tech Job Market Pipeline ===")

    #Step 1: Extract jobs from Adzuna.
    print("\nStep 1: Extracting jobs...")
    raw_jobs = extract_adzuna_jobs()

    #Step 2: Clean the extracted jobs.
    print("\nStep 2: Transforming jobs...")
    cleaned_jobs = transform_jobs(raw_jobs)

    print(f"Raw jobs received: {len(raw_jobs)}")
    print(f"Cleaned jobs prepared: {len(cleaned_jobs)}")

    #Save the cleaned jobs to the processed JSON file.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            cleaned_jobs,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Cleaned jobs saved to: {OUTPUT_FILE}")

    
    #Step 3: Load cleaned jobs into SQLite.
    print("\nStep 3: Loading jobs...")
    load_jobs(cleaned_jobs)

    print("\n=== Pipeline completed successfully ===")


if __name__ == "__main__":
    main()
