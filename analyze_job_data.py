import sqlite3
from pathlib import Path

DATABASE_FILE = Path("data/processed/jobs.db")


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        cursor = connection.cursor()

        print("\n=== Adzuna Job Data Quality Report ===")

        # Count all Adzuna jobs.
        total_jobs = cursor.execute(
            "SELECT COUNT(*) FROM adzuna_jobs"
        ).fetchone()[0]

        print(f"\nTotal Adzuna jobs: {total_jobs}")

        #Check missing values in important fields.
        fields = {
            "title": "title",
            "company": "company",
            "location": "location",
            "date_posted": "date_posted",
            "job_url": "job_url",
        }

        print("\nMissing values:")

        for label, column in fields.items():
            missing = cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM adzuna_jobs
                WHERE {column} IS NULL OR TRIM({column}) = ''
                """
            ).fetchone()[0]

            print(f"{label}: {missing}")

        #Count records with salary information.
        salary_count = cursor.execute(
            """
            SELECT COUNT(*)
            FROM adzuna_jobs
            WHERE salary_min IS NOT NULL
               OR salary_max IS NOT NULL
            """
        ).fetchone()[0]

        print(f"\nJobs with salary information: {salary_count}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
