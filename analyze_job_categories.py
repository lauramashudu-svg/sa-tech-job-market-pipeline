import sqlite3
from pathlib import Path

DATABASE_FILE = Path("data/processed/jobs.db")


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        query = """
            SELECT
                COALESCE(category, 'Unknown') AS job_category,
                COUNT(*) AS total_jobs
            FROM adzuna_jobs
            GROUP BY COALESCE(category, 'Unknown')
            ORDER BY total_jobs DESC, job_category ASC
        """

        results = connection.execute(query).fetchall()

        print("\n=== Adzuna Jobs by Category ===")

        for category, total in results:
            print(f"{category}: {total}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
