from typing import List, Tuple, Any, Optional, Union, Dict
from ..dependencies import (
    SQLCondition,
    ensure_sql_expression,
    no_condition,
    SQLExpression
)
from .formatters import (
    SQLCol,
    _normalize_column,
    _format_table_name,
    format_set_clause,
    _format_or_clause,
    _format_returning,
    _validate_col_names,
)
from expressql.base import ensure_col
from .utils import validate_monolist
from .formatters import format_conditions
from .formatters import _all_have_same_keys


def build_insert_query(
    table_name: str,
    values: Union[Dict[str, Any], List[Dict[str, Any]]],
    or_action: Optional[str] = None,
    on_conflict: Optional["OnConflictQuery"] = None,
    returning: Optional[Union[SQLCol, List[SQLCol]]] = None,
    ignore_forbidden_chars: bool = False,
) -> Tuple[str, List[Any]]:
    """
    Builds an INSERT SQL query with optional conflict handling and returning clause.

    Args:
        table_name: The name of the table.
        values: A dict of column-value pairs or a list of such dicts.
        or_action: Optional OR action like "REPLACE" or "IGNORE".
        on_conflict: Optional OnConflictQuery instance.
        returning: Optional returning clause.

    Returns:
        A tuple of (query string, parameters list).
    """
    # --- Normalize table ---
    table_name = _format_table_name(table_name, validate=not ignore_forbidden_chars)

    # --- Normalize values ---
    if isinstance(values, dict):
        values = [values]
    if not values:
        raise ValueError("At least one row of values must be provided.")
    if not _all_have_same_keys(values):
        raise ValueError("All value dictionaries must have the same keys.")

    # --- Extract columns ---
    col_names = list(values[0].keys())
    _validate_col_names(col_names)  # Reuse your validation
    col_list = [_normalize_column(col, ignore_forbidden_chars=ignore_forbidden_chars) for col in col_names]
    column_str = ", ".join(col_list)

    # --- Prepare placeholders and parameters ---
    rows_placeholder = []
    all_params = []
    for row in values:
        row_exprs = [ensure_sql_expression(row[col]) for col in col_names]
        ph_strings = []
        row_params = []
        for expr in row_exprs:
            ph, params = expr.placeholder_pair()
            ph_strings.append(ph)
            row_params.extend(params)
        rows_placeholder.append(f"({', '.join(ph_strings)})")
        all_params.extend(row_params)

    values_clause = ", ".join(rows_placeholder)

    # --- OR action ---
    or_clause = _format_or_clause(or_action)

    # --- ON CONFLICT ---
    if on_conflict:
        conflict_clause, conflict_params = on_conflict.placeholder_pair()
    else:
        conflict_clause, conflict_params = "", []
    all_params.extend(conflict_params)

    # --- RETURNING ---
    returning_clause = _format_returning(returning, ignore_forbidden_chars)

    # --- Final query ---
    query = (
        f"INSERT{or_clause} INTO {table_name} ({column_str}) VALUES {values_clause} {conflict_clause}{returning_clause}"
    )

    return query, all_params


class OnConflictQuery:
    """
    Class to handle ON CONFLICT clauses in SQL queries.

    Example usage:
        OnConflictQuery("Nothing")

    """

    valid_do_what = {"UPDATE", "NOTHING"}

    def __init__(
        self,
        do_what: str,
        conflict_cols: List[str],
        set_clauses: Union[List[Tuple], Dict] = None,
        condition: SQLCondition = None,
    ) -> None:
        self.DO(do_what)
        self.SET(set_clauses)
        self.WHERE(condition)
        conflict_cols = [ensure_col(col) for col in conflict_cols]
        self._conflict_cols = conflict_cols

    @property
    def conflict_cols(self) -> List[SQLCol]:
        return self._conflict_cols

    @conflict_cols.setter
    def conflict_cols(self, value: List[SQLCol]) -> None:
        if isinstance(value, (str, SQLExpression)):
            value = [value]
            return
        elif not isinstance(value, list):
            raise TypeError("Conflict columns must be a list of SQLCol objects.")
        validate_monolist(*value, monotype=SQLCol)
        conflict_cols = [ensure_col(col) for col in value]
        self._conflict_cols = conflict_cols

    def __repr__(self):
        return f"<OnConflictQuery do_what='{self.do_what}'>"

    def WHERE(self, condition: SQLCondition) -> "OnConflictQuery":
        if not isinstance(condition, SQLCondition) and condition is not None:
            raise TypeError("Condition must be an instance of SQLCondition.")
        self.condition = condition
        return self

    def DO(self, do_what: str) -> "OnConflictQuery":
        if do_what.upper() not in self.valid_do_what:
            raise ValueError(f"Invalid action: {do_what}. Valid actions are: {self.valid_do_what}")
        self.do_what = do_what.upper()
        return self

    def SET(self, *args, **kwargs) -> "OnConflictQuery":
        if not args and not kwargs:
            return self
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        set_dict = {}
        for arg in args:
            if isinstance(arg, dict):
                set_dict.update(arg)
            elif isinstance(arg, (tuple, list)) and len(arg) == 2:
                if isinstance(arg[0], SQLCol):
                    set_dict[arg[0].expression_value] = arg[1]
                    continue
                set_dict[arg[0]] = arg[1]
        set_dict.update(kwargs)
        self.set_clauses = set_dict
        print(set_dict)
        return self

    def placeholder_pair(self) -> str:
        """
        Returns a string representation of the ON CONFLICT clause.
        """
        if self.do_what == "NOTHING":
            return "ON CONFLICT DO NOTHING", []
        elif self.do_what == "UPDATE":
            if not self.condition:
                condition = no_condition
            else:
                condition = self.condition
            set_clause, injections = format_set_clause(self.set_clauses)
            condition_clause, condition_injections = format_conditions(condition)
            injections.extend(condition_injections)
            on_conflict_clause = (
                f'ON CONFLICT ({", ".join([col.expression_value for col in self.conflict_cols])}) '
                f'DO UPDATE {set_clause}{condition_clause}'
            )
            return on_conflict_clause, injections
        else:
            raise ValueError(f"Unknown conflict action: {self.do_what}")
