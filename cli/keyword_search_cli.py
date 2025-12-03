#!/usr/bin/env python3

import argparse
import json
from movies_model import MoviesData

MOVIES_FILEPATH = "./data/movies.json"

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

def keyword_search(keyword: str, max_results: int) -> MoviesData:

    with open(MOVIES_FILEPATH, 'r') as file:
        data = json.load(file)

    movies_data = MoviesData.from_dict(data)
    found_movies = MoviesData()

    for this_movie in movies_data.movies:
        if keyword in this_movie.title:
            found_movies.movies.append(this_movie)
        if len(found_movies.movies) >= max_results:
            break

    found_movies.movies = sorted(found_movies.movies, key=lambda movie: movie.id, reverse=True)
    return found_movies

if __name__ == '__main__':
    main()
