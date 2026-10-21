
"""
Transform raw Adzuna job listings into a consistent structure.
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "adzuna_jobs.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "adzuna_jobs_clean.json"


def transform_jobs(jobs):
    """Clean and standardise a list of Adzuna job listings."""

    cleaned_jobs = []

    for job in jobs:
        # Extract nested company and location information.
        company = job.get("company") or {}
        location = job.get("location") or {}
        category = job.get("category") or {}

        # Build one clean record for each job.
        cleaned_job = {
            "job_id": str(job.get("id") or ""),
            "job_title": (job.get("title") or "").strip(),
            "company_name": company.get("display_name"),
            "location": location.get("display_name"),
            "category": category.get("label"),
            "date_posted": job.get("created"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "salary_is_predicted": job.get("salary_is_predicted"),
            "job_url": job.get("redirect_url"),
            "description": (job.get("description") or "").strip(),
        }

        # Add the cleaned record to our list.
        cleaned_jobs.append(cleaned_job)

    return cleaned_jobs


def main():
    """Read raw JSON, transform the jobs, and save cleaned JSON."""

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw Adzuna file not found: {RAW_FILE}"
        )

    # Read the original API response.
    with RAW_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    jobs = data.get("results", [])

    # Transform the job listings.
    cleaned_jobs = transform_jobs(jobs)

    # Make sure the output folder exists.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save the cleaned records.
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(cleaned_jobs, file, indent=4, ensure_ascii=False)

    print("Adzuna transformation complete!")
    print(f"Raw jobs received: {len(jobs)}")
    print(f"Cleaned jobs saved: {len(cleaned_jobs)}")
    print(f"Output file: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
