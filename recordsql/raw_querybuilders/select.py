# record_queries/select.py

from typing import List, Tuple, Any, Optional, Union
from ..dependencies import SQLCondition
from ..utils import All
from .formatters import (
    SQLCol,
    SQLOrderBy,
    collect_column_placeholders,
    _format_conditions,
    _format_group_by,
    _format_having,
    _format_limit_offset,
    _format_order_by,
    _format_table_name,
)
from ..validators import validate_name


def build_select_query(
    table_name: str,
    columns: Union[All, List[SQLCol], str] = All(),
    condition: Optional[SQLCondition] = None,
    order_by: Optional[Union[SQLOrderBy, List[SQLOrderBy]]] = None,
    criteria: Union[str, List[str]] = "DESC",
    limit: Optional[Union[int, str]] = None,
    offset: Optional[Union[int, str]] = None,
    group_by: Union[SQLCol, List[SQLCol], None] = None,
    having: Optional[SQLCondition] = None,
    joins: Optional[List["JoinQuery"]] = None,  # type hint correction
    ignore_forbidden_chars: bool = False,
) -> Tuple[str, List[Any]]:
    columns_str, column_placeholders = collect_column_placeholders(columns, ignore_forbidden_chars)

    where_clause, where_params = _format_conditions(condition)
    group_by_clause = _format_group_by(group_by, ignore_forbidden_chars)
    having_clause, having_params = _format_having(having)
    order_str = _format_order_by(order_by, criteria)
    limit_offset_str = _format_limit_offset(limit, offset)

    table_name = _format_table_name(table_name, validate=not ignore_forbidden_chars)
    query = f"SELECT {columns_str} FROM {table_name}"
    join_clauses, join_params = _format_joins(joins)  # Correct return unpacking
    query += join_clauses
    query += where_clause
    query += group_by_clause
    query += having_clause
    query += order_str + limit_offset_str

    all_params = column_placeholders + where_params + join_params + having_params
    return query, all_params


class JoinQuery:
    def __init__(
        self,
        table_name: str,
        on: SQLCondition,
        join_type: str = "INNER",
        alias: Optional[str] = None,
        ignore_forbidden_chars: bool = False,
    ):
        join_type = join_type.upper()
        if join_type not in {"INNER", "LEFT", "RIGHT", "FULL", "CROSS"}:
            raise ValueError(f"Unsupported join type: {join_type}")

        validate_name(table_name, validate_chars=not ignore_forbidden_chars, allow_digit=True)
        if alias:
            validate_name(alias, validate_chars=not ignore_forbidden_chars)

        self.table_name = table_name
        self.on = on
        self.join_type = join_type
        self.alias = alias
        self.ignore_forbidden_chars = ignore_forbidden_chars

    def placeholder_pair(self) -> Tuple[str, List[Any]]:
        condition_str, params = self.on.placeholder_pair()
        table_expr = _format_table_name(self.table_name, validate=not self.ignore_forbidden_chars)
        if self.alias:
            table_expr = f"{table_expr} AS {self.alias}"

        return f"{self.join_type} JOIN {table_expr} ON {condition_str}", params


def _format_joins(joins: Optional[List[JoinQuery]]) -> Tuple[str, List[Any]]:
    if not joins:
        return "", []
    join_clauses = []
    join_params = []
    for join in joins:
        clause, params = join.placeholder_pair()
        join_clauses.append(clause)
        join_params.extend(params)
    return " " + " ".join(join_clauses), join_params
