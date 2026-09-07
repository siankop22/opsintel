from app.retrieval.vector_search import vector_search
from app.retrieval.keyword_search import keyword_search


def hybrid_search(session, query: str, limit: int = 3):
    vector_results = vector_search(session, query, limit=limit)
    keyword_results = keyword_search(session, query, limit=limit)

    scores = {}
    documents = {}

    for rank, doc in enumerate(vector_results):
        documents[doc.id] = doc
        scores[doc.id] = scores.get(doc.id, 0) + 1 / (60 + rank)

    for rank, doc in enumerate(keyword_results):
        documents[doc.id] = doc
        scores[doc.id] = scores.get(doc.id, 0) + 1 / (60 + rank)

    ranked_ids = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )

    return [
        documents[doc_id]
        for doc_id in ranked_ids[:limit]
    ]
