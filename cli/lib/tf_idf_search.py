from lib.clean_keywords import clean_keywords
from lib.inverted_index import InvertedIndex


def tf_search(doc_id: int, term: str) -> int:

    movie_index = InvertedIndex()
    term = clean_keywords(term)
    return movie_index.get_tf(doc_id, term[0])

def idf_search(term: str) -> float:

    movie_index = InvertedIndex()
    term = clean_keywords(term)[0]
    return movie_index.get_idf(term)

def tfidf_search(doc_id: int, term: str) -> float:

    tf = tf_search(doc_id, term)
    idf = idf_search(term)
    return tf * idf

def bm25idf_search(term: str) -> float:

    movie_index = InvertedIndex()
    term = clean_keywords(term)[0]
    return movie_index.get_bm25_idf(term)

def bm25tf_search(doc_id: int, term: str) -> float:

    movie_index = InvertedIndex()
    term = clean_keywords(term)[0]
    return movie_index.get_bm25_tf(doc_id, term)