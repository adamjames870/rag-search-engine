from enum import Enum

class Command(Enum):
    SEARCH = "search"
    BUILD = "build"
    TF = "tf"
    IDF = "idf"
    TFIDF = "tfidf"

class Arguments(Enum):
    TERM = "term"
    DOC_ID = "doc_id"
