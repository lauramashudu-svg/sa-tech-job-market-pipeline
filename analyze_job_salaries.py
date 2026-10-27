
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

        percentage = salary_jobs / total * 100 if total else 0

        console.print(
            Panel.fit(
                "[bold cyan]SA TECH JOB MARKET[/bold cyan]\n"
                "[white]Salary analysis[/white]",
                border_style="bright_blue",
            )
        )

        console.print(
            Panel(
                f"Total listings: [bold cyan]{total}[/bold cyan]\n"
                f"Listings with salary data: [bold green]{salary_jobs}[/bold green]\n"
                f"Salary data coverage: [bold yellow]{percentage:.1f}%[/bold yellow]",
                title="Salary Overview",
                border_style="magenta",
            )
        )

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

        table = Table(
            title="Listings with Salary Information",
            title_style="bold magenta",
            header_style="bold cyan",
            border_style="bright_blue",
        )

        table.add_column("Job Title", style="white")
        table.add_column("Location", style="cyan")
        table.add_column("Minimum Salary", justify="right", style="green")
        table.add_column("Maximum Salary", justify="right", style="green")
        table.add_column("Predicted?", justify="center")

        for title, location, minimum, maximum, predicted in rows:
            table.add_row(
                title or "Unknown",
                location or "Unknown",
                f"{minimum:,.2f}" if minimum is not None else "N/A",
                f"{maximum:,.2f}" if maximum is not None else "N/A",
                "Yes" if predicted else "No",
            )

        if rows:
            console.print(table)
        else:
            console.print(
                Panel(
                    "[yellow]No salary information is available in this dataset.[/yellow]",
                    title="No Salary Records",
                    border_style="yellow",
                )
            )

    finally:
        connection.close()


if __name__ == "__main__":
    main()
