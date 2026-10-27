
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

theme = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "heading": "bold magenta",
})

console = Console(theme=theme)


def show_banner():
    console.print(
        Panel.fit(
            "[bold cyan]SA TECH JOB MARKET PIPELINE[/bold cyan]\n"
            "[white]Extract • Transform • Load • Analyse[/white]",
            border_style="bright_blue",
        )
    )


def show_step(step_name, message):
    console.print(f"[heading]{step_name}[/heading] {message}")


def show_success(message):
    console.print(f"[success]✓ {message}[/success]")


def show_warning(message):
    console.print(f"[warning]⚠ {message}[/warning]")


def show_error(message):
    console.print(f"[error]✗ {message}[/error]")
