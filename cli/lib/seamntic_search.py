from sentence_transformers import SentenceTransformer

class SemanticSearch:

    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')


def verify_model() -> bool:
    sem_search = SemanticSearch()
    print(f"Model loaded: {sem_search.model}")
    print(f"Max sequence length: {sem_search.model.max_seq_length}")
    return True