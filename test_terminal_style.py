from src.terminal_style import (
    show_banner,
    show_step,
    show_success,
    show_warning,
    show_error,
)

show_banner()

show_step("EXTRACT", "Reading saved job data")
show_step("TRANSFORM", "Cleaning job records")
show_step("LOAD", "Saving records to SQLite")

show_success("Terminal styling is working!")
show_warning("Some job listings may have missing salary data.")
show_error("This is an example error message.")
