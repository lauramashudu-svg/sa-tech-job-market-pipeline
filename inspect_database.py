import sqlite3
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

DATABASE_FILE = Path("data/processed/jobs_recovered.db")

console = Console()


def main():
    console.print(
        Panel.fit(
            "[bold cyan]SA TECH JOB MARKET[/bold cyan]\n"
            "[white]Database inspection[/white]",
            border_style="bright_blue",
        )
    )

    console.print(
        f"Database file: [cyan]{DATABASE_FILE}[/cyan]"
    )

    if not DATABASE_FILE.exists():
        console.print(
            "[bold red]Database file not found.[/bold red]"
        )
        return

    console.print("[bold green]Database file exists.[/bold green]")

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        query = """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """

        tables = connection.execute(query).fetchall()

        if not tables:
            console.print(
                "[yellow]No user-defined tables were found.[/yellow]"
            )
            return

        console.print(
            f"\n[bold green]Tables found:[/bold green] {len(tables)}"
        )

        for (table_name,) in tables:
            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()

            table = Table(
                title=f"Table: {table_name}",
                title_style="bold magenta",
                header_style="bold cyan",
                border_style="bright_blue",
            )

            table.add_column("Column", style="white")
            table.add_column("Data Type", style="cyan")
            table.add_column("Required", justify="center")
            table.add_column("Primary Key", justify="center")

            for column in columns:
                name = column[1]
                data_type = column[2] or "Not specified"
                required = "Yes" if column[3] else "No"
                primary_key = "Yes" if column[5] else "No"

                table.add_row(
                    name,
                    data_type,
                    required,
                    primary_key,
                )

            console.print(table)

    finally:
        connection.close()


if __name__ == "__main__":
    main()
