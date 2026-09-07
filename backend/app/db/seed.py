from app.db.database import SessionLocal
from app.db.models import Document
from app.retrieval.embeddings import embed_text


DOCUMENTS = [
    {
        "title": "NYC-02 Packing Station Incident",
        "content": """
On September 4, packing stations 12 through 16 experienced
a conveyor control failure between 2:05 PM and 4:47 PM.

The outage reduced packing capacity by approximately 21 percent.
Maintenance replaced a failed controller and restarted the affected
stations at 4:47 PM.
"""
    },
    {
        "title": "NYC-02 Staffing Report",
        "content": """
The afternoon shift on September 4 had 88 employees scheduled.

Only 77 employees reported for work.

Packing experienced the largest staffing shortage with
approximately 12 percent fewer workers than planned.
"""
    },
    {
        "title": "NYC-02 Throughput Report",
        "content": """
Average throughput during the first week of September was
8,420 units per hour.

On September 4, throughput dropped to 6,870 units per hour
between 2 PM and 5 PM.

Throughput returned to normal levels after 5 PM.
"""
    },
]


def seed():
    session = SessionLocal()

    try:
        existing = session.query(Document).count()

        if existing > 0:
            print("Documents already exist.")
            return

        for item in DOCUMENTS:
            combined_text = f"{item['title']}\n{item['content']}"

            document = Document(
                title=item["title"],
                content=item["content"],
                embedding=embed_text(combined_text),
            )

            session.add(document)

        session.commit()
        print(f"Inserted {len(DOCUMENTS)} documents.")

    finally:
        session.close()


if __name__ == "__main__":
    seed()
