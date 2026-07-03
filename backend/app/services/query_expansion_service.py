EXPANSIONS = {
    "salary": [
        "salary",
        "pay",
        "compensation",
        "wages",
    ],
    "employee": [
        "employee",
        "staff",
        "worker",
        "personnel",
    ],
    "country": [
        "country",
        "nation",
        "location",
    ],
    "countries": [
        "countries",
        "nations",
        "locations",
    ],
}


def expand_query(
    query: str,
):
    expanded = []

    for word in query.lower().split():
        if word in EXPANSIONS:
            expanded.extend(
                EXPANSIONS[word]
            )
        else:
            expanded.append(
                word
            )

    return " ".join(
        expanded
    )