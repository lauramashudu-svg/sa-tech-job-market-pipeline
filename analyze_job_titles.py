import sqlite3
from pathlib import Path

DATABASE_FILE = Path("data/processed/jobs.db")


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        query = """
            SELECT
                title,
                COUNT(*) AS total_jobs
            FROM adzuna_jobs
            WHERE title IS NOT NULL
              AND TRIM(title) != ''
            GROUP BY title
            ORDER BY total_jobs DESC, title ASC
            LIMIT 15
        """

        results = connection.execute(query).fetchall()

        print("\n=== Most Common Adzuna Job Titles ===")

        for title, total in results:
            print(f"{title}: {total}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
