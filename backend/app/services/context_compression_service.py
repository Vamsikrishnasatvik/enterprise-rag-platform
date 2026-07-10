from collections import OrderedDict


def compress_context(
    chunks: list[dict],
    max_chunks: int = 6,
    min_length: int = 100,
) -> list[dict]:
    """
    Compress retrieved context.

    - Remove duplicates
    - Remove very small chunks
    - Keep highest scoring chunks
    """

    if not chunks:
        return []

    # Highest score first
    chunks = sorted(
        chunks,
        key=lambda chunk: chunk.get(
            "score",
            0,
        ),
        reverse=True,
    )

    unique = OrderedDict()

    for chunk in chunks:

        content = chunk.get(
            "content",
            "",
        ).strip()

        if len(content) < min_length:
            continue

        if content in unique:
            continue

        unique[content] = chunk

    return list(unique.values())[
        :max_chunks
    ]