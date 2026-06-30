def build_context(results):
    context = "\n\n".join(
        result.payload["content"]
        for result in results
    )

    MAX_CONTEXT_CHARS = 4000

    return context[:MAX_CONTEXT_CHARS]