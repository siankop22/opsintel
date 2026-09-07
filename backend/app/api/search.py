from fastapi import APIRouter, Query

from app.db.database import SessionLocal
from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank


router = APIRouter()


@router.get("/search")
def search(
    q: str = Query(..., min_length=2),
    limit: int = 3,
):
    session = SessionLocal()

    try:
        documents = hybrid_search(
            session,
            q,
            limit=10,
        )

        results = rerank(
            q,
            documents,
            limit=limit,
        )

        return {
            "query": q,
            "results": results,
        }

    finally:
        session.close()
