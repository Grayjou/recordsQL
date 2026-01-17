try:
    from tablesqlite import SQLTableInfo
except ImportError:
    raise ImportError(
        "tablesqlite is required for this integration. Please install it with: pip install recordsql[tablesqlite]"
    )
from .exists import exists_query
from .insert import insert_query
from .update import update_query
from .delete import delete_query
from .select import select_query
from .count import count_query


def add_query_methods(cls: type[SQLTableInfo] = SQLTableInfo) -> type[SQLTableInfo]:
    """
    Adds record-level query builder methods to a SQLTableInfo-derived class.

    This includes: insert_query, update_query, delete_query, select_query, count_query, exists_query.
    """
    cls.insert_query = insert_query
    cls.update_query = update_query
    cls.delete_query = delete_query
    cls.select_query = select_query
    cls.count_query = count_query
    cls.exists_query = exists_query
    return cls
