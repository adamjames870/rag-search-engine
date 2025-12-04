#!/usr/bin/env python3

import argparse

from lib.seamntic_search import verify_model
from models.commands import SemSearchCommand


def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest='command', help="Available commands")

    subparsers.add_parser(SemSearchCommand.VERIFY.value, help="Verify model")

    args = parser.parse_args()

    match args.command:
        case SemSearchCommand.VERIFY.value:
            verify_model()
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()