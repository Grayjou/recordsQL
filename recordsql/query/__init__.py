"""
Query builder module for recordsql.

This module provides the main query builder classes and functions for creating
SQL queries in a fluent, composable way.

Key Classes:
    - SELECT, SelectQuery, WITH, WithQuery, JoinQuery: For SELECT queries
    - INSERT, InsertQuery, OnConflictQuery: For INSERT queries
    - UPDATE, UpdateQuery: For UPDATE queries
    - DELETE, DeleteQuery: For DELETE queries
    - COUNT, CountQuery: For COUNT queries
    - EXISTS, ExistsQuery: For EXISTS queries

Example:
    >>> from recordsql import SELECT, cols
    >>> name, age = cols("name", "age")
    >>> query = SELECT(name, age).FROM("users").WHERE(age > 18)
    >>> print(query.placeholder_pair())
"""
# QueryBuilds/query/record_queries/__init__.py
from .select import SELECT, SelectQuery, WITH, WithQuery, JoinQuery
from .insert import INSERT, InsertQuery, OnConflictQuery
from .update import UPDATE, UpdateQuery
from .delete import DELETE, DeleteQuery
from .count import COUNT, CountQuery
from .exists import EXISTS, ExistsQuery

__all__ = [
    "SELECT",
    "WITH",
    "SelectQuery",
    "WithQuery",
    "JoinQuery",
    "InsertQuery",
    "INSERT",
    "OnConflictQuery",
    "UpdateQuery",
    "UPDATE",
    "DeleteQuery",
    "DELETE",
    "CountQuery",
    "COUNT",
    "ExistsQuery",
    "EXISTS",
]
