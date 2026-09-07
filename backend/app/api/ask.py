from fastapi import APIRouter
from pydantic import BaseModel

from app.db.database import SessionLocal
from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank
from app.services.rag import answer_with_context


router = APIRouter()


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(request: AskRequest):
    session = SessionLocal()

    try:
        documents = hybrid_search(
            session,
            request.question,
            limit=10,
        )

        evidence = rerank(
            request.question,
            documents,
            limit=3,
        )

        answer = answer_with_context(
            request.question,
            evidence,
        )

        return {
            "question": request.question,
            "answer": answer,
            "evidence": evidence,
        }

    finally:
        session.close()
