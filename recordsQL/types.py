"""
Type definitions for recordsQL.

This module defines common type aliases used throughout recordsQL for type hints
and improved code clarity.

Type Aliases:
    - SQLCol: Column type (str or SQLExpression)
    - SQLInput: Input type for SQL values
    - SQLOrderBy: Type for ORDER BY clauses
"""
from expressQL import SQLExpression, SQLCondition, no_condition, ensure_sql_expression
from typing import Union, List, Dict, Any

SQLCol = Union[str, SQLExpression]
SQLInput = Union[SQLCol, str, int, float]
SQLOrderBy = SQLCol
