import os
import pickle
from collections import defaultdict

from lib.clean_keywords import clean_keywords
from lib.search_utils import load_movies
from models.movies_model import Movie

class InvertedIndex:
    index: dict[str, set[int]]
    docmap: dict[int, Movie]

    INDEX_FILE = "cache/index.pkl"
    DOCMAP_FILE = "cache/docmap.pkl"

    def __init__(self):
        self.index: defaultdict[str, set[int]] = defaultdict(set)
        self.docmap: defaultdict[int, Movie] = defaultdict(Movie)

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

    def get_documents(self, word) -> list[int]:
        return sorted(self.index[word])

    def get_movie(self, id: int) -> Movie:
        return self.docmap[id]

    @staticmethod
    def force_rebuild() -> "InvertedIndex":
        files_to_delete = [InvertedIndex.INDEX_FILE, InvertedIndex.DOCMAP_FILE]
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

    def __save(self) -> None:
        os.makedirs("cache", exist_ok=True)
        with open(self.INDEX_FILE, "wb") as f:
            pickle.dump(self.index, f)
        with open(self.DOCMAP_FILE, "wb") as f:
            pickle.dump(self.docmap, f)

    def __load(self) -> None:
        """Load index and docmap from disk; raise FileNotFoundError if missing."""
        if not os.path.exists(self.INDEX_FILE):
            raise FileNotFoundError(f"{self.INDEX_FILE} not found")
        if not os.path.exists(self.DOCMAP_FILE):
            raise FileNotFoundError(f"{self.DOCMAP_FILE} not found")

        with open(self.INDEX_FILE, "rb") as f:
            self.index = pickle.load(f)
        with open(self.DOCMAP_FILE, "rb") as f:
            self.docmap = pickle.load(f)