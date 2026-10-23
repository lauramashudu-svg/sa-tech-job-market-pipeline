import sqlite3
from pathlib import Path

DATABASE_FILE = Path("data/processed/jobs.db")


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        total = connection.execute(
            "SELECT COUNT(*) FROM adzuna_jobs"
        ).fetchone()[0]

        salary_jobs = connection.execute(
            """
            SELECT COUNT(*)
            FROM adzuna_jobs
            WHERE salary_min IS NOT NULL
               OR salary_max IS NOT NULL
            """
        ).fetchone()[0]

        print("\n=== Adzuna Salary Analysis ===")
        print(f"Total job listings: {total}")
        print(f"Listings with salary data: {salary_jobs}")

        if total:
            percentage = salary_jobs / total * 100
            print(f"Salary data coverage: {percentage:.1f}%")

        print("\nJobs with salary information:")

        rows = connection.execute(
            """
            SELECT title, location, salary_min, salary_max,
                   salary_is_predicted
            FROM adzuna_jobs
            WHERE salary_min IS NOT NULL
               OR salary_max IS NOT NULL
            ORDER BY salary_min
            """
        ).fetchall()

        if not rows:
            print("No salary information available.")
        else:
            for title, location, minimum, maximum, predicted in rows:
                print(f"\nTitle: {title}")
                print(f"Location: {location}")
                print(f"Minimum salary: {minimum}")
                print(f"Maximum salary: {maximum}")
                print(f"Salary predicted: {predicted}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
