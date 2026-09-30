import logging
import os

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from services.llm import process_chat_request

EXIT_COMMANDS = ("exit", "quit", "bye")
ANSWER_PREFIX = "Response: "

logging.getLogger("google_genai").setLevel(logging.ERROR)

console = Console()

def ask(query: str) -> str:
    with console.status("[bold green]thinking", spinner="dots"):
        answer = process_chat_request(query).removeprefix(ANSWER_PREFIX)
    return answer


def print_answer(answer: str):
    console.print(Panel(Markdown(answer), title="Bot", title_align="left", border_style="green"))


def main():
    os.system("cls" if os.name == "nt" else "clear")
    console.print("[bold]College Info Bot[/bold]")
    console.print("[dim]Type 'exit' to quit.[/dim]\n")

    while True:
        try:
            query = console.input("[bold cyan]You[/bold cyan] > ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye!")
            break

        if not query:
            continue

        if query.lower() in EXIT_COMMANDS:
            console.print("Bye!")
            break

        try:
            answer = ask(query)
        except Exception as e:
            console.print(f"[bold red]Bot:[/bold red] [red]something went wrong -> {e}[/red]")
            continue

        print_answer(answer)


if __name__ == "__main__":
    main()
