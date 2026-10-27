import sqlite3
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

DATABASE_FILE = Path("data/processed/jobs_recovered.db")

console = Console()

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

        console.print(
            Panel.fit(
                "[bold cyan]SA TECH JOB MARKET[/bold cyan]\n"
                "[white]Jobs grouped by location[/white]",
                border_style="bright_blue",
            )
        )

        table = Table(
            title="Job Locations",
            title_style="bold magenta",
            header_style="bold cyan",
            border_style="bright_blue",
        )

        table.add_column("Location", style="white")
        table.add_column("Number of Jobs", justify="right", style="bold green")

        for location, total in results:
            table.add_row(location, str(total))

        console.print(table)

        total_jobs = sum(total for _, total in results)
        console.print(
            f"\n[bold green]Total locations found:[/bold green] {len(results)}"
        )

        console.print(
            f"[bold green]Total jobs counted:[/bold green] {total_jobs}"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()
