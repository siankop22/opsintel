from rank_bm25 import BM25Okapi

from app.db.models import Document


def keyword_search(session, query: str, limit: int = 3):
    documents = session.query(Document).all()

    if not documents:
        return []

    corpus = [
        f"{doc.title} {doc.content}".lower().split()
        for doc in documents
    ]

    bm25 = BM25Okapi(corpus)

    query_tokens = query.lower().split()
    scores = bm25.get_scores(query_tokens)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    return [doc for doc, score in ranked[:limit]]
