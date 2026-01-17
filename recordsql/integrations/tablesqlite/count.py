from typing import Union, List, Optional

try:
    from tablesqlite import SQLTableInfo
except ImportError:
    raise ImportError(
        "tablesqlite is required for this integration. Please install it with: pip install recordsql[tablesqlite]"
    )
from ...dependencies import SQLCondition, no_condition
from ...query import COUNT, CountQuery
from ...types import SQLCol


def count_query_for(
    table: SQLTableInfo,
    condition: Optional[SQLCondition] = no_condition,
    group_by: Union[SQLCol, List[SQLCol], None] = None,
    having: Optional[SQLCondition] = None,
) -> "CountQuery":
    """
    Create a reference for a COUNT query.
    """
    return COUNT(table_name=table.name).WHERE(condition).GROUP_BY(group_by).HAVING(having)


def count_query(
    self: SQLTableInfo,
    condition: Optional[SQLCondition] = no_condition,
    group_by: Union[SQLCol, List[SQLCol], None] = None,
    having: Optional[SQLCondition] = None,
    ignore_forbidden_characters: bool = False,
) -> "CountQuery":
    """
    Create a COUNT query reference for the table with the provided parameters.
    """
    return count_query_for(
        self,
        condition=condition,
        group_by=group_by,
        having=having,
        ignore_forbidden_characters=ignore_forbidden_characters,
    )
