try:
    from tablesqlite import SQLTableInfo
except ImportError:
    raise ImportError(
        "tablesqlite is required for this integration. Please install it with: pip install recordsql[tablesqlite]"
    )
from ...query import (
    SelectQuery,
    SELECT,
    WithQuery,
    JoinQuery,
)
from ...types import SQLCol
from typing import Union, List, Any, Optional
from ...dependencies import SQLCondition


def select_query_for(
    table: SQLTableInfo,
    columns: Union[str, List[SQLCol]] = "*",
    condition: SQLCondition = None,
    order_by: Optional[List[Any]] = None,
    criteria: List[str] = None,
    limit: Optional[Union[int, str]] = None,
    offset: Optional[Union[int, str]] = None,
    group_by: Union[Any, list, None] = None,
    having: Optional[Any] = None,
    *,
    joins: List[JoinQuery] = None,
    withs: Optional[List[WithQuery]] = None,
) -> SelectQuery:
    # Cant apply if_column_exists here, because columns can be any expression
    sq = SELECT(*columns).FROM(table.name).WHERE(condition).LIMIT(limit).OFFSET(offset).HAVING(having)
    sq.order_by = order_by
    sq.criteria = criteria
    sq.group_by = group_by
    sq.joins = joins or []
    sq.withs = withs or []
    return sq


def select_query(
    self: SQLTableInfo,
    columns: Union[str, List[SQLCol]] = "*",
    condition: Any = None,
    order_by: Optional[List[Any]] = None,
    criteria: List[str] = None,
    limit: Optional[Union[int, str]] = None,
    offset: Optional[Union[int, str]] = None,
    group_by: Union[Any, list, None] = None,
    having: Optional[Any] = None,
    *,
    joins: List[Any] = None,
    withs: Optional[List[WithQuery]] = None,
) -> SelectQuery:
    """
    Create a SELECT query for the table with the provided parameters.
    """
    return select_query_for(
        self,
        columns=columns,
        condition=condition,
        order_by=order_by,
        criteria=criteria,
        limit=limit,
        offset=offset,
        group_by=group_by,
        having=having,
        joins=joins,
        withs=withs,
    )
