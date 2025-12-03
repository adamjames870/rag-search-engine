#!/usr/bin/env python3

import argparse
from lib.keyword_search import keyword_search

def main() -> None:
    parser = argparse.ArgumentParser(description='Keyword Search CLI')
    subparsers = parser.add_subparsers(dest='command', help="Available commands")

    search_parser = subparsers.add_parser('search', help='Search movies using BM25')
    search_parser.add_argument('query', type=str, help='Search query')

    args = parser.parse_args()

    match args.command:
        case 'search':
            found_movies = keyword_search(args.query, 5)
            i = 1
            for movie in found_movies.movies:
                print(f'{i}. {movie.title}')
                i += 1
            pass
        case _:
            parser.print_help()



if __name__ == '__main__':
    main()
