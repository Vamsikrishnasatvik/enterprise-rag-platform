from sqlalchemy import text

from app.db.session import SessionLocal


def bm25_search(
    query: str,
    tenant_id: int | None = None,
    limit: int = 5,
    metadata_filters: dict | None = None,
):
    """
    PostgreSQL Full-Text Search.

    Returns normalized chunk dictionaries.
    """

    db = SessionLocal()

    try:

        sql = text(
            """
            SELECT
                id,
                document_id,
                content,
                ts_rank_cd(
                    to_tsvector('english', content),
                    plainto_tsquery('english', :query)
                ) AS score

            FROM document_chunks

            WHERE
                to_tsvector('english', content)
                @@
                plainto_tsquery('english', :query)

            ORDER BY score DESC

            LIMIT :limit
            """
        )

        results = db.execute(
            sql,
            {
                "query": query,
                "limit": limit,
            },
        )

        chunks = []

        for row in results:

            row = row._mapping

            chunks.append(
                {
                    "chunk_id": row["id"],
                    "document_id": row["document_id"],
                    "content": row["content"],
                    "score": float(row["score"]),
                    "page_number": None,
                    "section": None,
                }
            )

        return chunks

    finally:

        db.close()