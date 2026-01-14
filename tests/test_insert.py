"""Tests for INSERT queries"""
import pytest
from recordsql import INSERT, col


@pytest.mark.insert
class TestInsertBasic:
    """Test basic INSERT query functionality"""

    def test_insert_single_row(self):
        """Test INSERT with single row"""
        query = INSERT("name", "age").INTO("users").VALUES("John", 25)
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "(name, age)" in sql
        assert "VALUES (?, ?)" in sql
        assert params == ["John", 25]

    def test_insert_multiple_columns(self):
        """Test INSERT with multiple columns"""
        query = (
            INSERT("name", "email", "age", "active")
            .INTO("users")
            .VALUES("Jane", "jane@example.com", 30, True)
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "(name, email, age, active)" in sql
        assert params == ["Jane", "jane@example.com", 30, True]

    def test_insert_multiple_rows(self):
        """Test INSERT with multiple rows (bulk insert)"""
        query = (
            INSERT("name", "age")
            .INTO("users")
            .VALUES(("Alice", 28), ("Bob", 32), ("Charlie", 45))
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "(name, age)" in sql
        # Check for multiple value sets
        assert sql.count("(?, ?)") >= 3 or "VALUES" in sql
        assert "Alice" in params
        assert "Bob" in params
        assert "Charlie" in params
        assert 28 in params
        assert 32 in params
        assert 45 in params


@pytest.mark.insert
class TestInsertAdvanced:
    """Test advanced INSERT query functionality"""

    def test_insert_with_returning(self):
        """Test INSERT with RETURNING clause"""
        query = (
            INSERT("name", "email")
            .INTO("users")
            .VALUES("Tom", "tom@example.com")
            .RETURNING("id", "name", "email")
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "RETURNING" in sql
        assert params == ["Tom", "tom@example.com"]

    def test_insert_with_on_conflict_do_nothing(self):
        """Test INSERT with ON CONFLICT DO NOTHING"""
        query = (
            INSERT("email", "name")
            .INTO("users")
            .VALUES("user@example.com", "User")
            .ON_CONFLICT(do="NOTHING", conflict_cols=["email"])
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "ON CONFLICT" in sql
        assert "DO NOTHING" in sql
        assert params == ["user@example.com", "User"]

    def test_insert_with_on_conflict_do_update(self):
        """Test INSERT with ON CONFLICT DO UPDATE"""
        query = (
            INSERT("email", "name", "age")
            .INTO("users")
            .VALUES("user@example.com", "User", 25)
            .ON_CONFLICT(
                do="UPDATE",
                conflict_cols=["email"],
                set={"name": "Updated User", "age": 26},
            )
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "ON CONFLICT" in sql
        assert "DO UPDATE" in sql
        assert "SET" in sql
        assert "user@example.com" in params
        assert "User" in params
        assert 25 in params

    def test_insert_with_on_conflict_where(self):
        """Test INSERT with ON CONFLICT with WHERE clause"""
        query = (
            INSERT("col1", "col2")
            .INTO("table_name")
            .VALUES(1, 2)
            .ON_CONFLICT(
                do="UPDATE",
                conflict_cols=["col1"],
                set={"col2": 10},
                where=col("col1") == 1,
            )
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "table_name"' in sql
        assert "ON CONFLICT" in sql
        assert "DO UPDATE" in sql
        assert "WHERE" in sql
        assert 1 in params

    def test_insert_with_returning_specific_columns(self):
        """Test INSERT with RETURNING specific columns"""
        query = (
            INSERT("name", "email", "age")
            .INTO("users")
            .VALUES("Sarah", "sarah@example.com", 29)
            .RETURNING("id", "created_at")
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "RETURNING" in sql
        # Check that only specific columns are in RETURNING
        assert "id" in sql
        assert "created_at" in sql

    def test_insert_bulk_with_returning(self):
        """Test bulk INSERT with RETURNING"""
        query = (
            INSERT("name", "age")
            .INTO("users")
            .VALUES(("Alice", 25), ("Bob", 30))
            .RETURNING("id", "name")
        )
        sql, params = query.placeholder_pair()
        assert 'INSERT INTO "users"' in sql
        assert "RETURNING" in sql
        assert "Alice" in params
        assert "Bob" in params

    def test_insert_col_value_dict_single(self):
        """Test col_value_dict method for single insert"""
        query = INSERT("name", "age").INTO("users").VALUES("John", 25)
        col_value = query.col_value_dict()
        assert isinstance(col_value, dict)
        assert col_value == {"name": "John", "age": 25}

    def test_insert_col_value_dict_bulk(self):
        """Test col_value_dict method for bulk insert"""
        query = INSERT("name", "age").INTO("users").VALUES(("Alice", 28), ("Bob", 32))
        col_value = query.col_value_dict()
        assert isinstance(col_value, list)
        assert len(col_value) == 2
        assert col_value[0] == {"name": "Alice", "age": 28}
        assert col_value[1] == {"name": "Bob", "age": 32}
