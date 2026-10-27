
# Run the South African technology job market data pipeline.

import json

from rich.console import Console
from rich.panel import Panel

from src.extract.adzuna_api import extract_adzuna_jobs
from src.transform.transform_jobs import transform_jobs, OUTPUT_FILE
from src.load.load_jobs import load_jobs
from src.terminal_style import (
    show_banner,
    show_success,
    show_warning,
    show_error,
)

console = Console()


def main():
    """Extract, transform, and load job listings."""

    show_banner()

    try:
        # Step 1: Extract jobs from Adzuna.
        console.print("\n[bold cyan]STEP 1 — EXTRACT[/bold cyan]")
        console.print("Fetching job listings from Adzuna...")

        raw_jobs = extract_adzuna_jobs()
        show_success(f"Received {len(raw_jobs)} raw job records.")

        # Step 2: Transform the extracted jobs.
        console.print("\n[bold magenta]STEP 2 — TRANSFORM[/bold magenta]")
        console.print("Cleaning and preparing job records...")

        cleaned_jobs = transform_jobs(raw_jobs)

        console.print(f"Raw records: [cyan]{len(raw_jobs)}[/cyan]")
        console.print(f"Cleaned records: [cyan]{len(cleaned_jobs)}[/cyan]")

        # Save cleaned jobs to the processed JSON file.
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                cleaned_jobs,
                file,
                indent=4,
                ensure_ascii=False,
            )

        show_success(f"Cleaned data saved to {OUTPUT_FILE}")

        # Step 3: Load cleaned jobs into SQLite.
        console.print("\n[bold blue]STEP 3 — LOAD[/bold blue]")
        console.print("Saving job records to the database...")

        load_jobs(cleaned_jobs)
        show_success("Database loading step completed.")

        console.print(
            Panel.fit(
                "[bold green]PIPELINE COMPLETED SUCCESSFULLY[/bold green]\n"
                "[white]Extract • Transform • Load[/white]",
                border_style="green",
            )
        )

    except Exception as error:
        show_error(f"Pipeline failed: {error}")
        raise


if __name__ == "__main__":
    main()
