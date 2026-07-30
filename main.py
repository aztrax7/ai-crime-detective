#!/usr/bin/env python3
"""
Detective AI: The Case Files
A text-based detective game with a machine-learning guilt predictor.

Run:
    python main.py
"""

import sys

from game.case import Case
from game.detective import Detective
from game.investigation import GameSession

HELP_TEXT = """
Available commands:
  search                 - Search the crime scene for new evidence (cost 3)
  evidence               - List evidence you've discovered so far
  analyze <number>       - Closely examine a discovered evidence item (cost 1)
  suspects               - List all suspects and what you know about them
  profile <name>         - View a suspect's psychological profile
  interview <name>       - Question a suspect (cost 2)
  ai                     - Run the AI guilt-prediction analysis (cost 2)
  accuse <name>          - Accuse a suspect and end the case
  help                   - Show this help message
  quit                   - Quit the game
"""


def print_header():
    print("=" * 60)
    print("  DETECTIVE AI: THE CASE FILES")
    print("=" * 60)


def play_case(detective):
    case = Case()
    session = GameSession(case, detective)

    print()
    print(case.briefing())
    print()
    print("Suspects:")
    for s in case.suspects:
        print(f"  - {s.summary_line()}")
    print(HELP_TEXT)

    while not session.finished:
        print()
        print(detective.status_line())
        if detective.points <= 0:
            print("You're out of investigation points/time. You must accuse someone now.")

        try:
            raw = input("> ").strip()
        except EOFError:
            raw = "quit"

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "search":
            print(session.search_scene())
        elif cmd == "evidence":
            print(session.list_discovered())
        elif cmd == "analyze":
            if not arg.strip().isdigit():
                print("Usage: analyze <number>  (see 'evidence' for numbers)")
            else:
                print(session.analyze_evidence(int(arg.strip())))
        elif cmd == "suspects":
            print(session.check_database())
        elif cmd == "profile":
            if not arg:
                print("Usage: profile <suspect name>")
            else:
                print(session.suspect_profile(arg))
        elif cmd == "interview":
            if not arg:
                print("Usage: interview <suspect name>")
            else:
                print(session.interview(arg))
        elif cmd == "ai":
            print(session.run_ai_analysis())
        elif cmd == "accuse":
            if not arg:
                print("Usage: accuse <suspect name>")
            else:
                msg, correct = session.accuse(arg)
                print()
                print(msg)
        elif cmd == "help":
            print(HELP_TEXT)
        elif cmd in ("quit", "exit"):
            print("Leaving the case unsolved. Goodbye, detective.")
            sys.exit(0)
        else:
            print("Unknown command. Type 'help' for a list of commands.")

        if detective.points <= 0 and not session.finished:
            print("\nOut of time! You must type: accuse <suspect name>")


def main():
    print_header()
    print("Welcome, detective. A new case has just landed on your desk.")
    name = input("Enter your detective name (or press Enter for 'Detective'): ").strip()
    detective = Detective(name=name if name else "Detective")

    while True:
        play_case(detective)
        print()
        print(detective.status_line())
        again = input("Take on another case? (y/n): ").strip().lower()
        if again != "y":
            print(f"\nFinal score: {detective.score} | Final rank: {detective.rank()}")
            print("Thanks for playing Detective AI: The Case Files.")
            break


if __name__ == "__main__":
    main()
