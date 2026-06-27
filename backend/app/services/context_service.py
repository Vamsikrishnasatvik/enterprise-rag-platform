def build_context(
    results,
):
    contexts = []

    for result in results:
        contexts.append(
            result.payload["content"]
        )

    return "\n\n".join(
        contexts
    )