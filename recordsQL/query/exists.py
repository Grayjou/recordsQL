from ..base import RecordQuery
from ..types import SQLCol
from ..dependencies import SQLCondition, no_condition
from ..raw_querybuilders import build_exists_query
from typing import Optional, Union, List, Tuple, Any


class ExistsQuery(RecordQuery):
    name = "EXISTS"

    def __init__(
        self,
        table_name: str = None,
        condition: Optional[SQLCondition] = no_condition,
        group_by: Union[SQLCol, List[SQLCol], None] = None,
        having: Optional[SQLCondition] = None
    ):
        super().__init__(table_name=table_name, validate_table_name=False)
        self.condition = condition
        self.group_by = group_by
        self.having = having

    def FROM(self, table_name: str) -> "ExistsQuery":
        self.table_name = table_name
        return self

    def WHERE(self, condition: SQLCondition) -> "ExistsQuery":
        self.condition = condition
        return self

    def GROUP_BY(self, group_by: Union[SQLCol, List[SQLCol], None]) -> "ExistsQuery":
        self.group_by = group_by
        return self

    def HAVING(self, having: Optional[SQLCondition]) -> "ExistsQuery":
        self.having = having
        return self

    def placeholder_pair(self) -> Tuple[str, List[Any]]:
        return build_exists_query(
            table_name=self.table_name,
            condition=self.condition,
            group_by=self.group_by,
            having=self.having,
        )

    def __repr__(self):
        return f"ExistsQuery(table={self.table_name}, where={self.condition}, group_by={self.group_by}, having={self.having})"


def EXISTS(table_name: str = None) -> ExistsQuery:
    return ExistsQuery(table_name=table_name)
