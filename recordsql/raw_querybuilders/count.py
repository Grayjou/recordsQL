from typing import List, Tuple, Any, Optional, Union
from ..dependencies import SQLCondition
from .formatters import (
    SQLCol,
    _format_conditions,
    _format_group_by,
    _format_having,
    _format_table_name,
)


def build_count_query(
    table_name: str,
    condition: Optional[SQLCondition] = None,
    group_by: Union[SQLCol, List[SQLCol], None] = None,
    having: Optional[SQLCondition] = None,
    ignore_forbidden_chars: bool = False,
) -> Tuple[str, List[Any]]:
    """
    Builds a COUNT(*) SQL query with optional WHERE, GROUP BY and HAVING clauses.

    Args:
        table_name: The table to count rows from.
        condition: Optional WHERE condition.
        group_by: Optional GROUP BY columns.
        having: Optional HAVING condition.
        ignore_forbidden_chars: If True, skip name validation.

    Returns:
        Tuple of (query string, parameters list).
    """
    table_name = _format_table_name(table_name, validate=not ignore_forbidden_chars)

    where_clause, where_params = _format_conditions(condition)
    group_by_clause = _format_group_by(group_by, ignore_forbidden_chars)
    having_clause, having_params = _format_having(having)

    query = f"SELECT COUNT(*) FROM {table_name}{where_clause}{group_by_clause}{having_clause}"

    all_params = where_params + having_params

    return query, all_params
