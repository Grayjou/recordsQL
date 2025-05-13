from typing import Tuple, Any
from .select import build_select_query

def build_exists_query(
    table_name: str,
    condition = None,
    group_by = None,
    having = None,
) -> Tuple[str, list[Any]]:
    """
    Builds an EXISTS query.

    Args:
        table_name: The table to query.
        condition: Optional WHERE condition.
        group_by: Optional GROUP BY.
        having: Optional HAVING.
        ignore_forbidden_chars: Whether to skip validation.

    Returns:
        Tuple of (query string, parameters).
    """

    select_sql, params = build_select_query(
        table_name=table_name,
        columns="1",
        condition=condition,
        order_by=None,
        limit=1,  
        offset=None,
        group_by=group_by,
        having=having,
        ignore_forbidden_chars=True
    )

    query = f"SELECT EXISTS({select_sql})"

    return query, params

def _example():
    from expressQL import cols
    age = cols("age")[0]
    table = "employees"

    condition = age > 60

    query, params = build_exists_query(
        table_name=table,
        condition=condition
    )

    print(query)
    print("Params:", params)

if __name__ == "__main__":
    _example()
