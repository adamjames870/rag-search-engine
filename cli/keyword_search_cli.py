#!/usr/bin/env python3

import argparse

from lib.inverted_index import InvertedIndex
from lib.keyword_search import keyword_search
from lib.tf_idf_search import tf_search, idf_search, tfidf_search
from models.commands import Command, Arguments


def main() -> None:
    parser = argparse.ArgumentParser(description='Keyword Search CLI')
    subparsers = parser.add_subparsers(dest='command', help="Available commands")

    search_parser = subparsers.add_parser(Command.SEARCH.value, help='Search movies using BM25')
    search_parser.add_argument(Arguments.TERM.value, type=str, help='Search query')

    subparsers.add_parser(Command.BUILD.value, help='Build index')

    tf_parser = subparsers.add_parser(Command.TF.value, help='Search by tf')
    tf_parser.add_argument(Arguments.DOC_ID.value, type=int, help='Document ID (int)')
    tf_parser.add_argument(Arguments.TERM.value, type=str, help="Search term (single word)")

    idf_parser = subparsers.add_parser(Command.IDF.value, help='Find IDF')
    idf_parser.add_argument(Arguments.TERM.value, type=str, help="Search term (single word)")

    tfidf_parser = subparsers.add_parser(Command.TFIDF.value, help='Get combined tf/idf ranking')
    tfidf_parser.add_argument(Arguments.DOC_ID.value, type=int, help='Document ID (int)')
    tfidf_parser.add_argument(Arguments.TERM.value, type=str, help="Search term (single word)")

    args = parser.parse_args()

    match args.command:
        case Command.SEARCH.value:
            found_movies = keyword_search(args.term, 5)
            i = 1
            for movie in found_movies.movies:
                print(f'{i}. ID: {movie.id} | Title: {movie.title}')
                i += 1
            pass
        case Command.BUILD.value:
            index = InvertedIndex.force_rebuild()
            docs = index.get_documents("merida")
        case Command.TF.value:
            freq = tf_search(args.doc_id, args.term)
            print(freq)
        case Command.IDF.value:
            idf = idf_search(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case Command.TFIDF.value:
            tfidf = tfidf_search(args.doc_id, args.term)
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tfidf:.2f}")
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
