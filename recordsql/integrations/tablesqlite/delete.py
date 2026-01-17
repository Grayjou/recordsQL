try:
    from tablesqlite import SQLTableInfo
except ImportError:
    raise ImportError(
        "tablesqlite is required for this integration. Please install it with: pip install recordsql[tablesqlite]"
    )
from ...query import DeleteQuery, DELETE
from ...dependencies import SQLCondition, no_condition
from ...types import SQLCol
from typing import List


def delete_query_for(
    table: SQLTableInfo,
    condition: SQLCondition = no_condition,
    returning: List[SQLCol] = None,
) -> DeleteQuery:
    returning = returning or []
    return DELETE(table.name).WHERE(condition).RETURNING(*returning)


def delete_query(
    self: SQLTableInfo,
    condition: SQLCondition = no_condition,
    returning: List[SQLCol] = None,
) -> DeleteQuery:
    """
    Create a DELETE query for the table with the provided condition.
    """
    return delete_query_for(self, condition=condition, returning=returning)
