import math
import os
import pickle
from argparse import ArgumentError
from collections import defaultdict, Counter
from itertools import count

from lib.clean_keywords import clean_keywords, tokenise
from lib.search_utils import load_movies
from models.movies_model import Movie

class InvertedIndex:
    index: dict[str, set[int]]
    docmap: dict[int, Movie]
    term_frequencies: dict[int, Counter]

    INDEX_FILE = "cache/index.pkl"
    DOCMAP_FILE = "cache/docmap.pkl"
    TF_FILE = "cache/term_frequencies.pkl"

    def __init__(self):
        self.index: defaultdict[str, set[int]] = defaultdict(set)
        self.docmap: defaultdict[int, Movie] = defaultdict(Movie)
        self.term_frequencies: dict[int, Counter] = {}

        try:
            self.__load()
            print("Index loaded from disk")
        except FileNotFoundError:
            # If loading fails, build the index from scratch
            print("Failed to load index from disk, building new files")
            self.__build()
            self.__save()

    def __add_movie(self, doc_id: int, text: str) -> None:
        keywords = clean_keywords(text)
        for word in keywords:
            self.index[word].add(doc_id)
            self.__increment_term(doc_id, word)

    def __increment_term(self, doc_id: int, token: str):
        self.term_frequencies.setdefault(doc_id, Counter())[token] += 1

    def get_documents(self, word) -> list[int]:
        return sorted(self.index[word])

    def get_movie(self, id: int) -> Movie:
        return self.docmap[id]

    def get_tf(self, doc_id: int, term: str) -> int:
        if len(tokenise(term)) > 1:
            raise ValueError("more than one token")
        token = clean_keywords(term)[0]
        return self.term_frequencies.get(doc_id, Counter()).get(token, 0)

    def get_idf(self, term:str) -> float:
        doc_count = len(self.docmap)
        term_doc_count = len(self.index[term])
        print(f"doc_count: {doc_count} | term_doc_count: {term_doc_count}")
        return math.log((doc_count + 1) / (term_doc_count + 1))

    @staticmethod
    def force_rebuild() -> "InvertedIndex":
        files_to_delete = [
            InvertedIndex.INDEX_FILE,
            InvertedIndex.DOCMAP_FILE,
            InvertedIndex.TF_FILE
        ]
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass  # ignore if the file doesn't exist

        # Return a new instance (calls __init__)
        return InvertedIndex()

    def __build(self) -> None:
        movies = load_movies().movies
        for movie in movies:
            self.docmap[movie.id] = movie
            words = f"{movie.title} {movie.description}"
            self.__add_movie(movie.id, words)
        print(f"Analysed {len(self.docmap)} records")

    def __save(self) -> None:
        os.makedirs("cache", exist_ok=True)
        with open(self.INDEX_FILE, "wb") as f:
            pickle.dump(self.index, f)
        with open(self.DOCMAP_FILE, "wb") as f:
            pickle.dump(self.docmap, f)
        with open(self.TF_FILE, "wb") as f:
            pickle.dump(self.term_frequencies, f)

    def __load(self) -> None:
        """Load index and docmap from disk; raise FileNotFoundError if missing."""
        if not os.path.exists(self.INDEX_FILE):
            raise FileNotFoundError(f"{self.INDEX_FILE} not found")
        if not os.path.exists(self.DOCMAP_FILE):
            raise FileNotFoundError(f"{self.DOCMAP_FILE} not found")
        if not os.path.exists(self.TF_FILE):
            raise FileNotFoundError(f"{self.TF_FILE} not found")

        with open(self.INDEX_FILE, "rb") as f:
            self.index = pickle.load(f)
        with open(self.DOCMAP_FILE, "rb") as f:
            self.docmap = pickle.load(f)
        with open(self.TF_FILE, "rb") as f:
            self.term_frequencies = pickle.load(f)