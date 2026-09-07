from app.db.database import SessionLocal
from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank


def search_documents(query: str):
    session = SessionLocal()

    try:
        documents = hybrid_search(
            session,
            query,
            limit=10,
        )

        results = rerank(
            query,
            documents,
            limit=3,
        )

        return results

    finally:
        session.close()
