import sqlite3
from pathlib import Path

DATABASE_FILE = Path("data/processed/jobs.db")


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        query = """
            SELECT
                COALESCE(location, 'Unknown') AS job_location,
                COUNT(*) AS total_jobs
            FROM adzuna_jobs
            GROUP BY COALESCE(location, 'Unknown')
            ORDER BY total_jobs DESC, job_location ASC
        """

        results = connection.execute(query).fetchall()

        print("\n=== Adzuna Jobs by Location ===")

        for location, total in results:
            print(f"{location}: {total}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
