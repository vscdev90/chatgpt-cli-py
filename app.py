#!/usr/bin/env python3
"""
Simple ChatGPT CLI that talks to OpenAI's API.

Usage:
  python app.py --model gpt-4o-mini
  python app.py --model gpt-4o --system "Je bent een behulpzame assistent"
  python app.py --help
  
Set your API key via environment variable OPENAI_API_KEY or a .env file.
"""
import os
import sys
from typing import List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

try:
    import typer
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
except ImportError as e:
    print("Missing dependencies. Run: pip install -r requirements.txt", file=sys.stderr)
    raise

try:
    from openai import OpenAI
except Exception as e:
    print("OpenAI SDK not installed or import failed. Run: pip install -r requirements.txt", file=sys.stderr)
    raise

app = typer.Typer(add_completion=False, help=\"\"\"
Chat in your terminal with an OpenAI model.
- Stores conversation state in memory (optional: --no-memory for single-turn).
- Reads OPENAI_API_KEY from environment or .env file.
\"\"\")
console = Console()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def ensure_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        console.print(\"[bold red]OPENAI_API_KEY is not set[/]. Create a .env file or set the env var.\")
        raise typer.Exit(code=2)
    return key

@app.command()
def chat(
    model: str = typer.Option(DEFAULT_MODEL, help="Model name, e.g. gpt-4o, gpt-4o-mini"),
    system: str = typer.Option("Je bent een behulpzame assistent.", help="System prompt."),
    no_memory: bool = typer.Option(False, help="If set, do single-turn chats (stateless)."),
):
    \"\"\"Start an interactive chat session in your terminal.\"\"\"
    ensure_api_key()
    client = OpenAI()

    messages: List[dict] = [{"role": "system", "content": system}]

    console.print(Panel.fit(f\"Model: [bold]{model}[/]\\nType 'exit' or 'quit' to leave.\", title=\"ChatGPT CLI\"))

    while True:
        try:
            user_input = console.input(\"[bold cyan]You[/]: \")
        except (EOFError, KeyboardInterrupt):
            console.print(\"\\n[grey62]Bye![/]\")
            break

        if user_input.strip().lower() in {\"exit\", \"quit\"}:
            console.print(\"[grey62]Bye![/]\")
            break

        current_messages = messages if not no_memory else [{"role": "system", "content": system}]
        current_messages.append({"role": "user", "content": user_input})

        try:
            # Non-streaming for simplicity & reliability
            completion = client.chat.completions.create(
                model=model,
                messages=current_messages,
            )
            reply = completion.choices[0].message.content
        except Exception as e:
            console.print(f\"[bold red]API error:[/] {e}\")
            continue

        console.print(Markdown(reply))

        if not no_memory:
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": reply})

if __name__ == \"__main__\":
    app()
