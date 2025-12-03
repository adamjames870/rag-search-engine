from enum import Enum

class Command(Enum):
    SEARCH = "search"
    BUILD = "build"
    TF = "tf"
    IDF = "idf"
    TFIDF = "tfidf"
    BM25IDF = "bm25idf"
    BM25TF = "bm25tf"
    BM25SEARCH = "bm25search"

class Arguments(Enum):
    TERM = "term"
    DOC_ID = "doc_id"
