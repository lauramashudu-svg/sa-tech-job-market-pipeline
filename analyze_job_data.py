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
        cursor = connection.cursor()

        total_jobs = cursor.execute(
            "SELECT COUNT(*) FROM adzuna_jobs"
        ).fetchone()[0] 

        fields = {
            "Job Title": "title",
            "Company": "company",
            "Location": "location",
            "Date Posted": "date_posted",
            "Job URL": "job_url",
        }

        table = Table(
            title="Missing Values Report",
            title_style="bold magenta",
            header_style="bold cyan",
            border_style="bright_blue",
        )

        table.add_column("Field", style="white")
        table.add_column("Missing Records", justify="right")   
        table.add_column("Data Quality", justify="right")

        for label, column in fields.items():
            missing = cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM adzuna_jobs
                WHERE {column} IS NULL OR TRIM({column}) = ''
                """
            ).fetchone()[0]

            if missing == 0:
                status = "[bold green]Complete[/bold green]"
            else:
                status = "[bold yellow]Needs attention[/bold yellow]"

            table.add_row(label, str(missing), status)

        salary_count = cursor.execute(
            """
            SELECT COUNT(*)
            FROM adzuna_jobs
            WHERE salary_min IS NOT NULL
               OR salary_max IS NOT NULL
            """
        ).fetchone()[0]

        salary_percentage = (
            salary_count / total_jobs * 100 if total_jobs else 0
        )

        console.print(
            Panel.fit(
                "[bold cyan]SA TECH JOB MARKET[/bold cyan]\n"
                "[white]Data quality report[/white]",
                border_style="bright_blue",
            )
        )

        console.print(
            f"\n[bold]Total job listings:[/bold] [cyan]{total_jobs}[/cyan]"
        )
        console.print(table)

        console.print(
            Panel(
                f"Listings with salary data: [bold cyan]{salary_count}[/bold cyan]"
                f" out of {total_jobs}\n"
                f"Salary data coverage: [bold yellow]{salary_percentage:.1f}%[/bold yellow]",
                title="Salary Data Coverage",
                border_style="yellow",
            )
        )
    finally:
        connection.close()


if __name__ == "__main__":
    main()
