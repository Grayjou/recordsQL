"""Tests for UPDATE queries"""
import pytest
from recordsQL import UPDATE, cols, col, set_expr
from recordsQL import UPDATE, col, cols


@pytest.mark.update
class TestUpdateBasic:
    """Test basic UPDATE query functionality"""

    def test_update_single_field(self):
        """Test UPDATE with single field"""
        query = UPDATE("users").SET(name="John Doe")
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "SET" in sql
        assert "name = ?" in sql
        assert params == ["John Doe"]

    def test_update_multiple_fields(self):
        """Test UPDATE with multiple fields"""
        query = UPDATE("users").SET(name="John Doe", age=30, email="john@example.com")
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "SET" in sql
        assert "name = ?" in sql
        assert "age = ?" in sql
        assert "email = ?" in sql
        assert "John Doe" in params
        assert 30 in params
        assert "john@example.com" in params

    def test_update_with_where(self):
        """Test UPDATE with WHERE clause"""
        query = UPDATE("users").SET(name="Jane Doe").WHERE(col("id") == 1)
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "SET name = ?" in sql
        assert "WHERE" in sql
        assert "id = ?" in sql
        assert "Jane Doe" in params
        assert 1 in params

    def test_update_with_multiple_conditions(self):
        """Test UPDATE with multiple WHERE conditions"""
        age = col("age")
        active = col("active")
        query = (
            UPDATE("users").SET(status="senior").WHERE((age > 50) & (active == True))
        )
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "WHERE" in sql
        assert "senior" in params
        assert 50 in params
        assert True in params


@pytest.mark.update
class TestUpdateAdvanced:
    """Test advanced UPDATE query functionality"""

    def test_update_with_returning(self):
        """Test UPDATE with RETURNING clause"""
        query = (
            UPDATE("users")
            .SET(name="John Doe", age=30)
            .WHERE(col("id") == 5)
            .RETURNING("id", "name", "age", "updated_at")
        )
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "RETURNING" in sql
        assert "id" in sql
        assert "John Doe" in params
        assert 30 in params
        assert 5 in params

    def test_update_with_complex_where(self):
        """Test UPDATE with complex WHERE conditions"""
        age, salary, department = cols("age", "salary", "department")
        query = (
            UPDATE("employees")
            .SET(bonus=5000)
            .WHERE(((age > 30) & (salary < 80000)) | (department == "Sales"))
        )
        sql, params = query.placeholder_pair()
        assert 'UPDATE "employees"' in sql
        assert "WHERE" in sql
        assert 5000 in params
        assert 30 in params
        assert 80000 in params
        assert "Sales" in params

    def test_update_increment_value(self):
        """Test UPDATE with expression (increment) - skipped, set_expr API unclear"""
        """This was a misunderstanding, set_expr is for IN SET clause, not for expressions in WHERE."""
        values = set_expr((1,2,3))
        query = UPDATE("counters").SET(count=col("count") + 1).WHERE(col("id").isin(values))
        sql, params = query.placeholder_pair()
        assert 'UPDATE "counters"' in sql
        assert "(?, ?, ?)" in sql
        assert 1 in params
        assert 2 in params
        assert 3 in params

    def test_update_with_numeric_condition(self):
        """Test UPDATE with numeric conditions"""
        price = col("price")
        query = UPDATE("products").SET(on_sale=True).WHERE(price < 50)
        sql, params = query.placeholder_pair()
        assert 'UPDATE "products"' in sql
        assert "WHERE" in sql
        assert True in params
        assert 50 in params

    def test_update_with_string_condition(self):
        """Test UPDATE with string conditions"""
        category = col("category")
        query = UPDATE("products").SET(featured=True).WHERE(category == "Electronics")
        sql, params = query.placeholder_pair()
        assert 'UPDATE "products"' in sql
        assert "WHERE" in sql
        assert True in params
        assert "Electronics" in params

    def test_update_all_rows(self):
        """Test UPDATE without WHERE (affects all rows)"""
        query = UPDATE("users").SET(notification_enabled=True)
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "SET" in sql
        # Should not have WHERE clause
        assert "WHERE" not in sql
        assert params == [True]

    def test_update_boolean_fields(self):
        """Test UPDATE with boolean values"""
        query = UPDATE("users").SET(active=True, verified=False).WHERE(col("id") == 10)
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert True in params
        assert False in params
        assert 10 in params

    def test_update_null_value(self):
        """Test UPDATE with NULL value"""
        query = UPDATE("users").SET(last_login=None).WHERE(col("email") == None)
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "last_login = ?" in sql
        assert None in params
        assert "email IS NULL" in sql
        assert None in params

    def test_update_with_returning_all(self):
        """Test UPDATE with RETURNING *"""
        query = (
            UPDATE("users").SET(status="active").WHERE(col("id") == 20).RETURNING("*")
        )
        sql, params = query.placeholder_pair()
        assert 'UPDATE "users"' in sql
        assert "RETURNING" in sql
        assert "active" in params
        assert 20 in params
