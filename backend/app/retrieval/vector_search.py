from app.db.models import Document
from app.retrieval.embeddings import embed_text


def vector_search(session, query: str, limit: int = 3):
    query_embedding = embed_text(query)

    results = (
        session.query(Document)
        .order_by(
            Document.embedding.cosine_distance(query_embedding)
        )
        .limit(limit)
        .all()
    )

    return results
