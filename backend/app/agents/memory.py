from app.db.database import SessionLocal
from app.db.models import InvestigationSession, InvestigationMessage


def ensure_session(session_id: str):
    db = SessionLocal()

    try:
        existing = (
            db.query(InvestigationSession)
            .filter(InvestigationSession.session_id == session_id)
            .first()
        )

        if existing is None:
            db.add(
                InvestigationSession(
                    session_id=session_id
                )
            )
            db.commit()

    finally:
        db.close()


def save_message(
    session_id: str,
    role: str,
    content: str,
):
    ensure_session(session_id)

    db = SessionLocal()

    try:
        db.add(
            InvestigationMessage(
                session_id=session_id,
                role=role,
                content=content,
            )
        )

        db.commit()

    finally:
        db.close()


def get_history(
    session_id: str,
    limit: int = 10,
):
    db = SessionLocal()

    try:
        rows = (
            db.query(InvestigationMessage)
            .filter(
                InvestigationMessage.session_id == session_id
            )
            .order_by(InvestigationMessage.id.asc())
            .limit(limit)
            .all()
        )

        return [
            {
                "role": row.role,
                "content": row.content,
            }
            for row in rows
        ]

    finally:
        db.close()
