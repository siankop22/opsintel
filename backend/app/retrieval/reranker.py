from functools import lru_cache
from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


@lru_cache
def get_reranker():
    return CrossEncoder(MODEL_NAME)


def rerank(query: str, documents, limit: int = 3):
    if not documents:
        return []

    model = get_reranker()

    pairs = [
        [query, f"{doc.title}\n{doc.content}"]
        for doc in documents
    ]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: float(x[1]),
        reverse=True,
    )

    return [
        {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "score": float(score),
        }
        for doc, score in ranked[:limit]
    ]
