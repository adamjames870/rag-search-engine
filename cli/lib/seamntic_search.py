from sentence_transformers import SentenceTransformer

class SemanticSearch:

    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_embedding(self, text: str):
        if text is None or text.strip() == "":
            raise ValueError("Text cannot be empty")

        lst_text = [text]
        embedding = self.model.encode(lst_text)
        return embedding[0]

def verify_model() -> bool:
    sem_search = SemanticSearch()
    print(f"Model loaded: {sem_search.model}")
    print(f"Max sequence length: {sem_search.model.max_seq_length}")
    return True

def embd_text(text: str):
    sem_search = SemanticSearch()
    embedding = sem_search.generate_embedding(text)
    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")