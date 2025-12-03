import string

from lib.search_utils import load_stopwords
from nltk.stem import PorterStemmer

def clean_keywords(keywords: str) -> list[str]:

    words = basic_clean(keywords)

    return words

def clean_titles(title: str) -> list[str]:

    words = basic_clean(title)

    return words

def remove_punctuation(text: str) -> str:
    table = str.maketrans('', '', string.punctuation)
    return text.translate(table)

def tokenise(text: str) -> list[str]:
    return [token for token in text.split() if token]

def basic_clean(text: str) -> list[str]:
    text = text.lower()
    text = remove_punctuation(text)
    tokens = tokenise(text)
    tokens  = remove_stopwords(tokens)
    words = stem_words(tokens)
    return words

def remove_stopwords(text: list[str]) -> list[str]:
    stopwords = set(load_stopwords())
    return [word for word in text if word not in stopwords]

def stem_words(text: list[str]) -> list[str]:
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in text]

