import json

from models.movies_model import MoviesData

MOVIES_FILEPATH = "./data/movies.json"
STOPWORDS_FILEPATH = "./data/stopwords.txt"
BM25_K1 = 1.5
BM25_B = 0.75

def load_movies() -> MoviesData:

    with open(MOVIES_FILEPATH, 'r') as file:
        data = json.load(file)

    return MoviesData.from_dict(data)

def load_stopwords() -> list[str]:
    with open(STOPWORDS_FILEPATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def keyword_in_words(keywords: list[str], words: list[str]) -> bool:
    return any(k in t for k in keywords for t in words)