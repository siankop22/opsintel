from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.investigator import investigate


router = APIRouter()


class InvestigationRequest(BaseModel):
    question: str
    session_id: str = "default"


@router.post("/investigate")
def run_investigation(request: InvestigationRequest):
    return investigate(
        request.question,
        session_id=request.session_id,
    )
