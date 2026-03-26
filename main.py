"""
Entrepreneurship & Innovation Intelligence Agent
CLI entrypoint.

Run:
    python main.py
"""

from agent import EntrepreneurshipAgent
from utils import banner, pretty_print
from rich.console import Console
from rich.prompt import Prompt

console = Console()


HELP_TEXT = """
**Commands**
- `reset`   — Clear conversation history and start fresh
- `help`    — Show this message
- `exit`    — Quit the agent

**What you can ask**
- "Run a Lean Canvas for my B2B SaaS idea: [description]"
- "Evaluate this startup idea: [description]"
- "How do I price a developer tool at pre-seed stage?"
- "What frameworks should I use to find product-market fit?"
"""


def main() -> None:
    banner()
    console.print("[dim]Type 'help' for commands, 'exit' to quit.[/]\n")

    agent = EntrepreneurshipAgent()

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/]")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            console.print("[dim]Goodbye![/]")
            break

        if user_input.lower() == "reset":
            agent.reset()
            console.print("[yellow]Conversation reset.[/]\n")
            continue

        if user_input.lower() == "help":
            pretty_print("Help", HELP_TEXT)
            continue

        with console.status("[bold cyan]Thinking…[/]", spinner="dots"):
            try:
                response = agent.chat(user_input)
            except Exception as exc:
                console.print(f"[red]Error:[/] {exc}")
                continue

        pretty_print("Agent", response)
        console.print()


if __name__ == "__main__":
    main()
