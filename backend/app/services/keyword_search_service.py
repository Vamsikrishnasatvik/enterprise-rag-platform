from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.document_chunk import (
    DocumentChunk,
)


def keyword_search(
    db: Session,
    tenant_id: int,
    query: str,
    limit: int = 10,
):
    sql = text(
        """
        SELECT
            id,
            ts_rank(
                to_tsvector('english', content),
                plainto_tsquery('english', :query)
            ) AS rank
        FROM document_chunks
        WHERE
            tenant_id = :tenant_id
            AND
            to_tsvector('english', content)
            @@
            plainto_tsquery(
                'english',
                :query
            )
        ORDER BY rank DESC
        LIMIT :limit
        """
    )

    rows = db.execute(
        sql,
        {
            "tenant_id": tenant_id,
            "query": query,
            "limit": limit,
        },
    ).fetchall()

    #
    # FALLBACK SEARCH
    #
    if not rows:
        first_word = query.split()[0]

        sql = text(
            """
            SELECT
                id,
                1.0 AS rank
            FROM document_chunks
            WHERE
                tenant_id = :tenant_id
                AND
                lower(content)
                LIKE
                lower(:pattern)
            LIMIT :limit
            """
        )

        rows = db.execute(
            sql,
            {
                "tenant_id": tenant_id,
                "pattern": f"%{first_word}%",
                "limit": limit,
            },
        ).fetchall()

    if not rows:
        return []

    chunk_ids = [
        row.id
        for row in rows
    ]

    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.tenant_id
            == tenant_id
        )
        .filter(
            DocumentChunk.id.in_(chunk_ids)
        )
        .all()
    )

    score_map = {
        row.id: float(row.rank)
        for row in rows
    }

    results = []

    for chunk in chunks:
        results.append(
            {
                "chunk": chunk,
                "score": score_map.get(
                    chunk.id,
                    1.0,
                ),
            }
        )

    return results