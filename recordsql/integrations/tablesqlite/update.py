try:
    from tablesqlite import SQLTableInfo
except ImportError:
    raise ImportError(
        "tablesqlite is required for this integration. Please install it with: pip install recordsql[tablesqlite]"
    )
from ...query import (
    UpdateQuery,
    UPDATE,
)
from ...types import SQLCol, SQLInput
from typing import List, Dict
from ...dependencies import SQLCondition, no_condition


def update_query_for(
    table: SQLTableInfo,
    set_clauses: Dict[str, SQLInput] = None,
    condition: SQLCondition = no_condition,
    returning: List[SQLCol] = None,
    if_column_exists: bool = True,
    resolve_by: str = "raise",
    **kwargs,
) -> UpdateQuery:
    initial_set_clauses = kwargs
    set_clauses_in_self = {key: value for key, value in initial_set_clauses.items() if key in table.column_dict}

    if set_clauses is not None:
        if not isinstance(set_clauses, dict):
            raise TypeError("set_clauses must be a dictionary.")
        set_clauses_in_self.update({key: value for key, value in set_clauses.items() if key in table.column_dict})
        initial_set_clauses.update(set_clauses)
    if if_column_exists and initial_set_clauses != set_clauses_in_self:
        if resolve_by.lower() == "raise":
            raise ValueError("If 'if_column_exists' is True, all provided columns must exist in the table.")
        elif resolve_by.lower() == "ignore":
            initial_set_clauses = set_clauses_in_self
        else:
            raise ValueError(f"Invalid resolve_by value: {resolve_by}")
    if not initial_set_clauses:
        raise ValueError("No valid columns provided for update.")
    returning = returning or []
    return UPDATE(table.name).SET(initial_set_clauses).WHERE(condition).RETURNING(*returning)


def update_query(
    self: SQLTableInfo,
    set_clauses: Dict[str, SQLInput] = None,
    condition: SQLCondition = no_condition,
    returning: List[SQLCol] = None,
    if_column_exists: bool = True,
    resolve_by: str = "raise",
    **kwargs,
) -> UpdateQuery:
    """
    Create an UPDATE query for the table with the provided data.
    """
    return update_query_for(
        self,
        set_clauses=set_clauses,
        condition=condition,
        returning=returning,
        if_column_exists=if_column_exists,
        resolve_by=resolve_by,
        **kwargs,
    )
