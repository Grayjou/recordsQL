try:
    from tablesqlite import SQLTableInfo
except ImportError:
    raise ImportError(
        "tablesqlite is required for this integration. Please install it with: pip install recordsql[tablesqlite]"
    )
from ...query import ExistsQuery, EXISTS
from ...types import SQLCol
from typing import List, Union, Optional
from ...dependencies import SQLCondition, no_condition


def exists_query_for(
    table: SQLTableInfo,
    condition: Optional[SQLCondition] = no_condition,
    group_by: Union[SQLCol, List[SQLCol], None] = None,
    having: Optional[SQLCondition] = None,
) -> "ExistsQuery":
    """
    Create a reference for an EXISTS query.
    """
    return EXISTS(table_name=table.name).WHERE(condition).GROUP_BY(group_by).HAVING(having)


def exists_query(
    self: SQLTableInfo,
    condition: Optional[SQLCondition] = no_condition,
    group_by: Union[SQLCol, List[SQLCol], None] = None,
    having: Optional[SQLCondition] = None,
) -> "ExistsQuery":
    """
    Create an EXISTS query reference for the table with the provided parameters.
    """
    return exists_query_for(self, condition=condition, group_by=group_by, having=having)
