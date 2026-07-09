from app.schemas.execution_plan import ExecutionPlan


def apply_planner_rules(
    plan: ExecutionPlan,
    question: str,
    history_length: int,
) -> ExecutionPlan:
    """
    Apply deterministic business rules to the
    execution plan.

    The LLM proposes a plan.
    These rules improve consistency.
    """

    question_lower = question.lower()

    # ----------------------------
    # Conversation Memory
    # ----------------------------

    if history_length > 0:
        plan.use_memory = True

    if plan.intent == "follow_up":
        plan.use_memory = True

    # ----------------------------
    # Retrieval Strategy
    # ----------------------------

    keyword_queries = [
        "faq",
        "section",
        "appendix",
        "document id",
        "policy number",
        "version",
        "code",
    ]

    semantic_queries = [
        "explain",
        "why",
        "how",
        "compare",
        "difference",
        "overview",
        "benefits",
    ]

    if any(
        keyword in question_lower
        for keyword in keyword_queries
    ):

        plan.search_strategy = "bm25"

    elif any(
        keyword in question_lower
        for keyword in semantic_queries
    ):

        plan.search_strategy = "semantic"

    else:

        plan.search_strategy = "hybrid"

    plan.use_hybrid_search = (
        plan.search_strategy == "hybrid"
    )

    # ----------------------------
    # Policy Questions
    # ----------------------------

    if "policy" in question_lower:
        plan.requires_verification = True
        plan.requires_reranking = True
        plan.retrieval_count = max(
            plan.retrieval_count,
            5,
        )

    # ----------------------------
    # Comparison Questions
    # ----------------------------

    if plan.intent == "comparison":
        plan.multi_document = True
        plan.retrieval_count = max(
            plan.retrieval_count,
            8,
        )

    # ----------------------------
    # Metadata Filters
    # ----------------------------

    if "hr" in question_lower:

        plan.use_metadata_filters = True

        plan.metadata_filters.setdefault(
            "department",
            "HR",
        )

    if "it" in question_lower:

        plan.use_metadata_filters = True

        plan.metadata_filters.setdefault(
            "department",
            "IT",
        )

    if "finance" in question_lower:

        plan.use_metadata_filters = True

        plan.metadata_filters.setdefault(
            "department",
            "Finance",
        )

    # ----------------------------
    # Definitions
    # ----------------------------

    if plan.intent == "definition":

        plan.retrieval_count = min(
            plan.retrieval_count,
            3,
        )

        plan.requires_reranking = False

    return plan