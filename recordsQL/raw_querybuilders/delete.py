from typing import List, Tuple, Any, Optional, Union
from ..dependencies import SQLCondition
from .formatters import _format_conditions, _format_table_name, _format_returning


def build_delete_query(
    table_name: str,
    condition: Optional[SQLCondition] = None,
    returning: Optional[Union[str, List[str]]] = None,
    ignore_forbidden_chars: bool = False,
) -> Tuple[str, List[Any]]:
    """
    Builds a DELETE SQL query.

    Args:
        table_name: The name of the table.
        condition: Optional WHERE condition.
        returning: Optional RETURNING clause.

    Returns:
        A tuple of (query string, parameters list).
    """
    table_name = _format_table_name(table_name, validate=not ignore_forbidden_chars)
    where_clause, where_params = _format_conditions(condition)
    returning_clause = _format_returning(returning, ignore_forbidden_chars)

    query = f"DELETE FROM {table_name}{where_clause}{returning_clause}"

    return query, where_params
