from app.services.query_expansion_service import (
    expand_query,
)

queries = expand_query(
    "What is the HR leave policy?"
)

print()

print("=" * 80)
print("QUERY EXPANSION")
print("=" * 80)

for query in queries:
    print("-", query)