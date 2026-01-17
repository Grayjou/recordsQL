# record_queries/formatters.py

from typing import Dict, Any, List, Tuple, Union, Optional
from collections.abc import Iterable
from ..dependencies import (
    SQLCondition,
    SQLExpression,
    FalseCondition,
    ensure_sql_expression,
)
from ..validators import validate_name
from ..utils import All
from ..base import RecordQuery

SQLCol = Union[str, SQLExpression, RecordQuery]  # Type alias for column names
SQLOrderBy = Union[str, SQLExpression]  # Type alias for order_by parameter


def _normalize_column(column: SQLCol, *, ignore_forbidden_chars: bool = False) -> str:
    if _is_all_columns(column):
        return "*"
    if isinstance(column, str):
        column = column.strip()
        if not ignore_forbidden_chars:
            validate_name(column)  # Validate the column name
        # this will run the validation of the column name
        return column
    elif isinstance(column, SQLExpression):
        if not column.expression_type == "column":
            raise TypeError("Column must be a string or a column expression.")
        return column.expression_value
    else:
        raise TypeError("Column must be a string or a column expression.")


def _collect_column_placeholder(column: SQLCol, ignore_forbidden_chars: bool = False) -> str:
    if isinstance(column, str):
        column = column.strip()
        if not ignore_forbidden_chars:
            validate_name(column)  # Validate the column name
        return column, []
    elif isinstance(column, (SQLExpression, RecordQuery)):
        return column.placeholder_pair()
    else:
        raise TypeError("Column must be a string or a column expression.")


def collect_column_placeholders(
    columns: Union[All, List[SQLCol], str], ignore_forbidden_chars: bool = False
) -> List[str]:
    if _is_all_columns(columns):
        return "*", []
    elif isinstance(columns, (str, SQLExpression)):
        col_list = [columns]
    elif isinstance(columns, (list, tuple)):
        col_list = columns
    else:
        raise TypeError("columns must be a list of strings, a string, or All().")
    collected_strings = []
    collected_placeholders = []
    for col in col_list:
        col_str, placeholders = _collect_column_placeholder(col, ignore_forbidden_chars=ignore_forbidden_chars)
        collected_strings.append(col_str)
        collected_placeholders.extend(placeholders)
    col_str = ", ".join(collected_strings)
    return col_str, collected_placeholders


def _is_all_columns(columns):
    # Check for explicit All type or standard "all columns" indicators
    if isinstance(columns, All):
        return True

    # Direct comparisons using 'is' and type checking to avoid SQLExpression __eq__ issues
    if columns is None:
        return True
    if isinstance(columns, str) and columns == "*":
        return True
    if isinstance(columns, list) and len(columns) == 0:
        return True

    # For list/tuple types, check if it's a single "*" string
    if isinstance(columns, (list, tuple)):
        if len(columns) == 1 and isinstance(columns[0], str) and columns[0] == "*":
            return True
        # Check if any element is None or a "*" string (avoid == for non-strings)
        return any(c is None or (isinstance(c, str) and c == "*") for c in columns)

    return False


def _format_columns(columns: Union[All, List[SQLCol], str], ignore_forbidden_chars: bool = False) -> str:
    if _is_all_columns(columns):
        return "*"
    elif isinstance(columns, SQLCol):
        col_list = [columns]
    elif isinstance(columns, (list, tuple)):
        col_list = columns
    else:
        raise TypeError("columns must be a list of strings, a string, or All().")

    columns = [_normalize_column(col, ignore_forbidden_chars=ignore_forbidden_chars) for col in col_list]
    col_str = ", ".join(columns)

    return col_str


format_columns = _format_columns  # Alias for backward compatibility


def _normalize_order_by(order_by: Union[str, SQLExpression]) -> str:
    if isinstance(order_by, str):
        return order_by
    elif isinstance(order_by, SQLExpression):
        if not order_by.is_column_expression():
            raise TypeError("order_by must be a string or a column expression.")
        return order_by.sql_string(include_sign_only_if_negative=True, invert=True)
    else:
        raise TypeError("order_by must be a string or a column expression.")


def _format_order_by(
    order_by: Optional[Union[SQLOrderBy, List[SQLOrderBy]]],
    criteria: Union[str, List[str]] = "DESC",
) -> str:
    if not order_by:
        return ""

    if not isinstance(order_by, list):
        order_by = [order_by]
    if not isinstance(criteria, list):
        criteria = [criteria] * len(order_by)  # Apply same criteria to all

    if len(order_by) != len(criteria):
        raise ValueError("Number of columns and criteria must match.")

    order_clauses = []
    for col, crit in zip(order_by, criteria):
        col_name = _normalize_order_by(col)
        crit = crit.strip().upper()
        if crit not in {"ASC", "DESC"}:
            crit = "DESC"
        order_clauses.append(f"{col_name} {crit}")

    return " ORDER BY " + ", ".join(order_clauses)


format_order_by = _format_order_by  # Alias for backward compatibility


def _format_limit_offset(limit: Optional[Union[int, str]], offset: Optional[Union[int, str]]) -> str:
    clauses = []
    if limit is not None:
        try:
            clauses.append(f"LIMIT {int(limit)}")
        except (ValueError, TypeError):
            raise ValueError("Limit must be an integer or a string representing an integer.")
    if offset is not None:
        try:
            clauses.append(f"OFFSET {int(offset)}")
        except (ValueError, TypeError):
            raise ValueError("Offset must be an integer or a string representing an integer.")
    return " " + " ".join(clauses) if clauses else ""


def column_string(column_list: Union[SQLCol, List[SQLCol]], *args: SQLCol) -> str:
    if column_list == "*":
        all_cols = "*"
    else:
        if isinstance(column_list, SQLCol):
            column_list = [column_list]
        elif isinstance(column_list, Iterable):
            column_list = list(column_list)
        else:
            column_list = [column_list]
        extra_args = [arg for arg in args if isinstance(arg, SQLCol)]

        all_cols = column_list + extra_args
    column_str = format_columns(all_cols)
    return column_str


def _format_conditions(condition: Optional[SQLCondition], *, default_false: bool = False) -> Tuple[str, List[Any]]:
    """
    Formats a WHERE clause and its parameters from a SQLCondition.

    Args:
        condition (Optional[SQLCondition]): The SQLCondition to process.
        default_false (bool): If True, returns a WHERE FALSE clause when no condition.

    Returns:
        Tuple[str, List[Any]]: (WHERE string, parameters list)
    """
    if condition and not isinstance(condition, FalseCondition):
        where_clause, where_params = condition.placeholder_pair()
        where_clause = f" WHERE {where_clause}"
        return where_clause, where_params
    elif default_false:
        return " WHERE 0=1", []  # Always false (could be used for defensive queries)
    else:
        return "", []


format_conditions = _format_conditions


def ensure_list(value: Any, *, decompose_string: bool = False, unpack_iterable: bool = False) -> List[Any]:
    """
    Ensures the input is returned as a list.

    - If `value` is a string and `decompose_string` is True, splits into characters.
    - If `value` is an iterable (excluding strings unless `decompose_string`), and `unpack_iterable` is
        True, unpacks it.
    - Otherwise, wraps the value in a list.
    """
    if isinstance(value, str):
        return list(value) if decompose_string else [value]

    if isinstance(value, Iterable) and unpack_iterable:
        return list(value)

    return [value]


def _validate_col_names(col_names: Iterable[str]) -> None:
    """
    Validates a list of column names using the same col validation.
    """
    if isinstance(col_names, str):
        col_names = [col_names]
    if not isinstance(col_names, Iterable):
        raise TypeError("Column names must be an iterable of strings.")
    for col_name in col_names:
        validate_name(col_name)


def normalize_update_values(values: Union[Dict[str, Any], List[tuple], tuple]) -> Dict[str, Any]:
    if isinstance(values, dict):
        return values
    elif isinstance(values, (list, tuple)):
        # Single pair case: ("column", value)
        if len(values) == 2 and isinstance(values[0], str):
            return {values[0]: values[1]}
        # Multiple pairs: [(col, val), ...]
        try:
            return dict(values)
        except Exception:
            raise TypeError("List/tuple values must be (column, value) pairs.")
    raise TypeError("Values must be a dict, a list of pairs, or a single (column, value) tuple.")


def _format_or_clause(action: Optional[str]) -> str:
    """
    Formats an OR conflict action clause.

    Args:
        action (Optional[str]): Action type like 'REPLACE', 'IGNORE', etc.

    Returns:
        str: OR clause part (e.g., 'OR REPLACE') or empty string if no action.
    """
    if action:
        return f" OR {action.strip().upper()}"
    return ""


def _format_returning(
    returning: Optional[Union[SQLCol, List[SQLCol]]],
    ignore_forbidden_chars: bool = False,
) -> str:
    """
    Formats a RETURNING clause.

    Args:
        returning: A single column, a list of columns, or None.
        ignore_forbidden_chars: Whether to skip name validation.

    Returns:
        A string like " RETURNING col1, col2" or "".
    """
    if not returning:
        return ""

    cols = ensure_list(returning, unpack_iterable=True)
    returning_cols = ", ".join(_normalize_column(col, ignore_forbidden_chars=ignore_forbidden_chars) for col in cols)
    return f" RETURNING {returning_cols}"


def _all_have_same_keys(dicts: List[Dict[str, Any]]) -> bool:
    """
    Check if all dictionaries in a list have the same keys.

    Args:
        dicts (List[Dict[str, Any]]): List of dictionaries to check.

    Returns:
        bool: True if all dictionaries have the same keys, False otherwise.
    """
    if not dicts:
        return True
    first_keys = set(dicts[0].keys())
    return all(set(d.keys()) == first_keys for d in dicts[1:])


def format_set_clause(values: Dict[str, Any]) -> Tuple[str, List[Any]]:
    """
    Formats a dictionary of column-value pairs into a SQL SET clause.

    Each value must support `.placeholder_pair()` which returns:
    - A SQL fragment (e.g. "col1 + col2" or "?")
    - A list of injection values

    Returns:
        A tuple of:
        - The SQL SET clause string
        - A flat list of all injection values
    """
    values = {key: ensure_sql_expression(value) for key, value in values.items()}

    parts_and_injections = [
        (f"{key} = {expr_str}", injections)
        for key, expr in values.items()
        for expr_str, injections in [expr.placeholder_pair()]
    ]

    set_clause = "SET " + ", ".join(part for part, _ in parts_and_injections)
    all_injections = [param for _, injections in parts_and_injections for param in injections]

    return set_clause, all_injections


def _format_group_by(
    group_by: Optional[Union[SQLCol, List[SQLCol]]],
    ignore_forbidden_chars: bool = False,
) -> str:
    if not group_by:
        return ""
    group_cols = ensure_list(group_by, unpack_iterable=True)
    group_cols_str = ", ".join(
        _normalize_column(col, ignore_forbidden_chars=ignore_forbidden_chars) for col in group_cols
    )
    return f" GROUP BY {group_cols_str}"


def _format_having(having: Optional[SQLCondition]) -> Tuple[str, List[Any]]:
    if having and not isinstance(having, FalseCondition):
        having_clause, having_params = having.placeholder_pair()
        return f" HAVING {having_clause}", having_params
    else:
        return "", []


quote_dict = {
    0: '"',
    1: "'",
}


def quote_sandwich(value: str, quote=0) -> str:
    if quote not in quote_dict:
        raise ValueError("Invalid quote type. Use 0 for double quotes or 1 for single quotes.")
    if not isinstance(value, str):
        raise TypeError("Value must be a string.")
    if not value:
        raise ValueError("Value cannot be empty.")
    thy_quote = quote_dict[quote]
    return f"{thy_quote}{value}{thy_quote}"


def isit_quoted(value: str, quote=0) -> bool:
    if quote not in quote_dict:
        raise ValueError("Invalid quote type. Use 0 for double quotes or 1 for single quotes.")
    thy_quote = quote_dict[quote]
    return value.startswith(thy_quote) and value.endswith(thy_quote)


def _format_table_name(table_name: str, validate=True) -> str:
    """
    Formats a table name for SQL queries.

    Args:
        table_name (str): The name of the table.

    Returns:
        str: The formatted table name.
    """
    if validate:
        validate_name(table_name, allow_dot=True, allow_dollar=False, allow_digit=True)
    if isit_quoted(table_name, 0):
        return table_name.strip()

    return quote_sandwich(table_name, 0)  # Add double quotes around the table name
