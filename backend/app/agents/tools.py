import os

from app.db.database import SessionLocal
from app.retrieval.hybrid import hybrid_search
from app.retrieval.keyword_search import keyword_search
from app.retrieval.reranker import rerank


def search_documents(query: str):
    session = SessionLocal()

    try:
        lightweight = os.getenv(
            "LIGHTWEIGHT_RETRIEVAL",
            "false",
        ).lower() == "true"

        if lightweight:
            documents = keyword_search(
                session,
                query,
                limit=3,
            )

            return [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "content": doc.content,
                    "score": None,
                }
                for doc in documents
            ]

        documents = hybrid_search(
            session,
            query,
            limit=10,
        )

        return rerank(
            query,
            documents,
            limit=3,
        )

    finally:
        session.close()
