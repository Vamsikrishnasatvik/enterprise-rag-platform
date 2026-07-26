from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_results(
    query: str,
    chunks,
):
    """
    Rerank retrieved chunks using a CrossEncoder.
    """

    if not chunks:
        return []

    pairs = [
        (
            query,
            chunk.payload["content"],
        )
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk.score = float(score)

    return sorted(
        chunks,
        key=lambda c: c.score,
        reverse=True,
    )