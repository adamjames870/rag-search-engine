#!/usr/bin/env python3

import argparse

from lib.inverted_index import InvertedIndex
from lib.keyword_search import keyword_search, bm25_search
from lib.search_utils import BM25_B
from lib.tf_idf_search import tf_search, idf_search, tfidf_search, bm25idf_search, bm25tf_search
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

    bm25idf_parser = subparsers.add_parser(Command.BM25IDF.value, help="Get BM25 IDF score for a given term")
    bm25idf_parser.add_argument(Arguments.TERM.value, type=str, help="Search term (single word)")

    bm25tf_parser = subparsers.add_parser(Command.BM25TF.value, help='Get BM25 TF score for a given term')
    bm25tf_parser.add_argument(Arguments.DOC_ID.value, type=int, help='Document ID (int)')
    bm25tf_parser.add_argument(Arguments.TERM.value, type=str, help="Search term (single word)")
    bm25tf_parser.add_argument("b", type=float, nargs='?', default=BM25_B, help="Tunable BM25 b parameter")

    bm25search_parser = subparsers.add_parser(Command.BM25SEARCH.value, help='Search movies using full BM25 scoring')
    bm25search_parser.add_argument(Arguments.TERM.value, type=str, help='Search query')

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
        case Command.BM25IDF.value:
            bm25idf = bm25idf_search(args.term)
            print(f"BM25 IDF score of '{args.term}': {bm25idf:.2f}")
        case Command.BM25TF.value:
            bm25tf = bm25tf_search(args.doc_id, args.term)
            print(f"BM25 TF score of '{args.term}' in document '{args.doc_id}': {bm25tf:.2f}")
        case Command.BM25SEARCH.value:
            results = bm25_search(args.term, 5)
            i = 1
            for movie in results:
                print(f'{i}. ({movie.id}) {movie.title} - Score: {movie.score:.2f}')
                i = i + 1
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
