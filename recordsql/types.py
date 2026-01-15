"""
Type definitions for recordsql.

This module defines common type aliases used throughout recordsql for type hints
and improved code clarity.

Type Aliases:
    - SQLCol: Column type (str or SQLExpression)
    - SQLInput: Input type for SQL values
    - SQLOrderBy: Type for ORDER BY clauses
"""
from expressql import SQLExpression
from typing import Union

SQLCol = Union[str, SQLExpression]
SQLInput = Union[SQLCol, str, int, float]
SQLOrderBy = SQLCol
