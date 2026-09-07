from sqlalchemy import text

from app.db.database import engine


def query_operations(site: str):
    sql = text("""
        SELECT
            site,
            timestamp,
            throughput,
            staffing,
            downtime_minutes
        FROM operations_metrics
        WHERE site = :site
        ORDER BY timestamp
    """)

    with engine.connect() as connection:
        rows = connection.execute(
            sql,
            {"site": site},
        ).mappings().all()

    return [dict(row) for row in rows]
