"""
Shared utility functions used across the project.
"""

import json
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


def pretty_print(title: str, content: str) -> None:
    """Render a titled panel with markdown content to the terminal."""
    console.print(Panel(Markdown(content), title=title, border_style="bright_blue"))


def safe_json_parse(text: str) -> dict[str, Any] | None:
    """Attempt to parse a JSON string; return None on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def truncate(text: str, max_chars: int = 300) -> str:
    """Truncate long strings for log output."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "…"


def banner() -> None:
    """Print the startup banner."""
    console.print(
        Panel(
            "[bold bright_cyan]Entrepreneurship & Innovation Intelligence Agent[/]\n"
            "[dim]Powered by LangGraph + Groq[/]",
            border_style="cyan",
        )
    )
