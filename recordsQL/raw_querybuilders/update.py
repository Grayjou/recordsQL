from typing import List, Tuple, Any, Optional, Union, Dict
from ..dependencies import SQLCondition
from .formatters import (
    SQLCol,
    _format_conditions,
    _format_table_name,
    format_set_clause,
    _format_returning,
)
from .formatters import normalize_update_values


def build_update_query(
    table_name: str,
    values: Union[Dict[str, Any], List[Tuple[str, Any]], Tuple[str, Any]],
    condition: Optional[SQLCondition] = None,
    returning: Optional[Union[SQLCol, List[SQLCol]]] = None,
    ignore_forbidden_chars: bool = False,
) -> Tuple[str, List[Any]]:
    """
    Builds an UPDATE SQL query.

    Args:
        table_name: Name of the table.
        values: Column-value pairs to update.
        condition: Optional WHERE clause.
        returning: Optional RETURNING clause.

    Returns:
        A tuple of (query string, parameters list).
    """
    table_name = _format_table_name(table_name, validate=not ignore_forbidden_chars)

    # Normalizar los valores
    values = normalize_update_values(values)
    set_clause, set_params = format_set_clause(values)

    where_clause, where_params = _format_conditions(condition)
    returning_clause = _format_returning(returning, ignore_forbidden_chars)

    query = f"UPDATE {table_name} {set_clause}{where_clause}{returning_clause}"

    all_params = set_params + where_params

    return query, all_params
