from datetime import datetime

from app.db.database import SessionLocal
from app.db.models import OperationsMetric


ROWS = [
    {
        "site": "NYC-02",
        "timestamp": datetime(2026, 9, 4, 13, 0),
        "throughput": 8350,
        "staffing": 88,
        "downtime_minutes": 0,
    },
    {
        "site": "NYC-02",
        "timestamp": datetime(2026, 9, 4, 14, 0),
        "throughput": 7100,
        "staffing": 78,
        "downtime_minutes": 35,
    },
    {
        "site": "NYC-02",
        "timestamp": datetime(2026, 9, 4, 15, 0),
        "throughput": 6650,
        "staffing": 77,
        "downtime_minutes": 60,
    },
    {
        "site": "NYC-02",
        "timestamp": datetime(2026, 9, 4, 16, 0),
        "throughput": 6860,
        "staffing": 77,
        "downtime_minutes": 47,
    },
    {
        "site": "NYC-02",
        "timestamp": datetime(2026, 9, 4, 17, 0),
        "throughput": 8290,
        "staffing": 80,
        "downtime_minutes": 0,
    },
]


def seed():
    session = SessionLocal()

    try:
        existing = session.query(OperationsMetric).count()

        if existing > 0:
            print("Operations metrics already exist.")
            return

        for row in ROWS:
            session.add(OperationsMetric(**row))

        session.commit()
        print(f"Inserted {len(ROWS)} operation metric rows.")

    finally:
        session.close()


if __name__ == "__main__":
    seed()
