#Run the South African technology job market data pipeline.


from src.extract.adzuna_api import extract_adzuna_jobs
from src.transform.transform_jobs import transform_jobs
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

    #Step 3: Load cleaned jobs into SQLite.
    print("\nStep 3: Loading jobs...")
    load_jobs(cleaned_jobs)

    print("\n=== Pipeline completed successfully ===")


if __name__ == "__main__":
    main()
