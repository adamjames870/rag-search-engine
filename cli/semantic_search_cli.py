#!/usr/bin/env python3

import argparse

from lib.seamntic_search import verify_model, embd_text
from models.commands import SemSearchCommand, Arguments


def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest='command', help="Available commands")

    subparsers.add_parser(SemSearchCommand.VERIFY.value, help="Verify model")

    embedtext_parser = subparsers.add_parser(SemSearchCommand.EMBED_TEXT.value, help="Embed text")
    embedtext_parser.add_argument(Arguments.TERM.value, type=str, help="Text to embed")

    args = parser.parse_args()

    match args.command:
        case SemSearchCommand.VERIFY.value:
            verify_model()
        case SemSearchCommand.EMBED_TEXT.value:
            embd_text(args.term)
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()