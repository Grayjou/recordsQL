try:
    from tablesqlite import SQLTableInfo
except ImportError:
    raise ImportError(
        "tablesqlite is required for this integration. Please install it with: pip install recordsql[tablesqlite]"
    )
from ...query import (
    InsertQuery,
    INSERT,
    OnConflictQuery,
)
from ...types import SQLCol
from typing import Union, Dict, Tuple, List, Any


def insert_query_for(
    table: SQLTableInfo,
    *items: Union[Dict, Tuple[str, Any]],
    or_action: str = None,
    on_conflict: OnConflictQuery = None,
    returning: List[SQLCol] = None,
    if_column_exists: bool = True,
    resolve_by: str = "raise",
    **kwargs,
) -> InsertQuery:
    set_columns = kwargs
    set_columns_in_self = {key: value for key, value in set_columns.items() if key in table.column_dict}
    for item in items:
        if isinstance(item, dict):
            set_columns_in_self.update({key: value for key, value in item.items() if key in table.column_dict})
            set_columns.update(item)
        elif isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str):
            set_columns[item[0]] = item[1]
            if item[0] in table.column_dict:
                set_columns_in_self[item[0]] = item[1]
        else:
            raise ValueError(f"Invalid item format: {item}. Expected dict or (str, any) tuple.")
    if if_column_exists and set_columns != set_columns_in_self:
        if resolve_by.lower() == "raise":
            raise ValueError("If 'if_column_exists' is True, all provided columns must exist in the table.")
        elif resolve_by.lower() == "ignore":
            set_columns = set_columns_in_self
    if not set_columns:
        raise ValueError("No valid columns provided for insertion.")
    returning = returning or []
    iq: InsertQuery = INSERT().INTO(table.name).SET(set_columns).RETURNING(*returning)
    if on_conflict is not None:
        iq = iq.ON_CONFLICT(
            do=on_conflict.do_what,
            conflict_cols=on_conflict.conflict_cols,
            set=on_conflict.set_clauses,
            where=on_conflict.condition,
        )
    iq.or_action = or_action
    return iq


def insert_query(
    self: SQLTableInfo,
    *items: Union[Dict, Tuple[str, Any]],
    or_action: str = None,
    on_conflict: OnConflictQuery = None,
    returning: List[SQLCol] = None,
    if_column_exists=True,
    resolve_by: str = "raise",
    **kwargs,
) -> InsertQuery:
    """
    Create an INSERT query for the table with the provided data.
    """
    return insert_query_for(
        self,
        *items,
        or_action=or_action,
        on_conflict=on_conflict,
        returning=returning,
        if_column_exists=if_column_exists,
        resolve_by=resolve_by,
        **kwargs,
    )
