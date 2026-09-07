from functools import lru_cache

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache
def get_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    model = get_embedding_model()
    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )
    return embedding.tolist()
