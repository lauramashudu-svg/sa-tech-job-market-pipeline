
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

        console.print(
            Panel.fit(
                "[bold cyan]SA TECH JOB MARKET[/bold cyan]\n"
                "[white]Most common job titles[/white]",
                border_style="bright_blue",
            )
        )

        table = Table(
            title="Top 15 Job Titles",
            title_style="bold magenta",
            header_style="bold cyan",
            border_style="bright_blue",
        )

        table.add_column("Rank", justify="right", style="yellow")
        table.add_column("Job Title", style="white")
        table.add_column("Number of Listings", justify="right", style="bold green")

        for rank, (title, total) in enumerate(results, start=1):
            table.add_row(str(rank), title, str(total))

        if results:
            console.print(table)
        else:
            console.print(
                "[yellow]No job titles were found in the database.[/yellow]"
            )

        console.print(
            f"\n[bold green]Unique job titles displayed:[/bold green] "
            f"{len(results)}"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()
