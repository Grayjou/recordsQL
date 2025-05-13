from expressQL import SQLExpression, SQLCondition, no_condition, ensure_sql_expression
from typing import Union, List, Dict, Any

SQLCol = Union[str, SQLExpression]
SQLInput = Union[SQLCol, str, int, float]
SQLOrderBy = SQLCol