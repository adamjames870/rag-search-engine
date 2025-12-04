import math
import os
import pickle
from collections import defaultdict, Counter

from lib.clean_keywords import clean_keywords, tokenise
from lib.search_utils import load_movies, BM25_K1, BM25_B
from models.movies_model import Movie


class InvertedIndex:
    index: dict[str, set[int]]
    docmap: dict[int, Movie]
    term_frequencies: dict[int, Counter]
    doc_lengths: dict[int, int] # doc_id vs count of tokens(terms/words)

    CACHE_DIR = "cache/"

    INDEX_FILE = os.path.join(CACHE_DIR, "index.pkl")
    DOCMAP_FILE = os.path.join(CACHE_DIR, "docmap.pkl")
    TF_FILE = os.path.join(CACHE_DIR, "term_frequencies.pkl")
    DOC_LENGTH_FILE = os.path.join(CACHE_DIR, "oc_lengths.pkl")

    def __init__(self):
        self.index: defaultdict[str, set[int]] = defaultdict(set)
        self.docmap: dict[int, Movie] = {}
        self.term_frequencies: dict[int, Counter] = {}
        self.doc_lengths: dict[int, int] = {}

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
        self.doc_lengths[doc_id] = len(keywords)
        for word in keywords:
            self.index[word].add(doc_id)
            self.__increment_term(doc_id, word)

    def __increment_term(self, doc_id: int, token: str):
        self.term_frequencies.setdefault(doc_id, Counter())[token] += 1

    def get_documents(self, word) -> list[int]:
        return sorted(self.index[word])

    def get_movie(self, doc_id: int) -> Movie:
            return self.docmap[doc_id]

    def __get_avg_doc_length(self) -> float:
        if not self.doc_lengths:
            return 0.0
        return sum(self.doc_lengths.values()) / len(self.doc_lengths)

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

    def get_bm25_idf(self, term: str) -> float:
        if len(tokenise(term)) > 1:
            raise ValueError("more than one token")
        token = clean_keywords(term)[0]
        N = len(self.docmap) #doc_count
        df =  len(self.index[token]) #count docs containing this term
        return math.log((N - df + 0.5) / (df + 0.5) + 1)

    def get_bm25_tf(self, doc_id, term, k1 = BM25_K1, b = BM25_B) -> float:
        raw_tf = self.get_tf(doc_id, term)

        doc_length = self.term_frequencies[doc_id].total()
        avg_doc_length = self.__get_avg_doc_length()
        length_norm = 1 - b + b * (doc_length / avg_doc_length)

        bm25_tf = (raw_tf * (k1 + 1)) / (raw_tf + k1 * length_norm)

        return bm25_tf

    def get_bm25(self, doc_id, term, k1 = BM25_K1, b = BM25_B) -> float:
        tf = self.get_bm25_tf(doc_id, term, k1, b)
        idf = self.get_bm25_idf(term)
        return tf * idf

    def bm25_search(self, query: str, limit: int) -> dict[int, float]:
        terms = clean_keywords(query)
        scores: dict[int, float] = {}
        for _, movie in self.docmap.items():
            score = 0
            for term in terms:
                score = score + self.get_bm25(movie.id, term)
            scores[movie.id] = score
        return dict(sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:limit])

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
        with open(self.DOC_LENGTH_FILE, "wb") as f:
            pickle.dump(self.doc_lengths, f)

    def __load(self) -> None:
        """Load index and docmap from disk; raise FileNotFoundError if missing."""
        if not os.path.exists(self.INDEX_FILE):
            raise FileNotFoundError(f"{self.INDEX_FILE} not found")
        if not os.path.exists(self.DOCMAP_FILE):
            raise FileNotFoundError(f"{self.DOCMAP_FILE} not found")
        if not os.path.exists(self.TF_FILE):
            raise FileNotFoundError(f"{self.TF_FILE} not found")
        if not os.path.exists(self.TF_FILE):
            raise FileNotFoundError(f"{self.DOC_LENGTH_FILE} not found")

        with open(self.INDEX_FILE, "rb") as f:
            self.index = pickle.load(f)
        with open(self.DOCMAP_FILE, "rb") as f:
            self.docmap = pickle.load(f)
        with open(self.TF_FILE, "rb") as f:
            self.term_frequencies = pickle.load(f)
        with open(self.DOC_LENGTH_FILE, "rb") as f:
            self.doc_lengths = pickle.load(f)