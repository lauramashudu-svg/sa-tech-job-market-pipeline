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
                COALESCE(category, 'Unknown') AS job_category,
                COUNT(*) AS total_jobs
            FROM adzuna_jobs
            GROUP BY COALESCE(category, 'Unknown')
            ORDER BY total_jobs DESC, job_category ASC
        """

        results = connection.execute(query).fetchall()

        console.print(
            Panel.fit(
                "[bold cyan]SA TECH JOB MARKET[/bold cyan]\n"
                "[white]Jobs grouped by category[/white]",
                border_style="bright_blue",
            )
        )

        table = Table(
            title="Job Categories",
            title_style="bold magenta",
            header_style="bold cyan",
            border_style="bright_blue",
        )

        table.add_column("Job Category", style="white")
        table.add_column("Total Jobs", justify="right", style="bold green")

        for category, total in results:
            table.add_row(category, str(total))

        console.print(table)

        console.print(
            f"\n[bold green]Total categories found:[/bold green] "
            f"{len(results)}"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()
