"""Tests for DELETE queries"""
import pytest
from recordsql import DELETE, col, cols, text


@pytest.mark.delete
class TestDeleteBasic:
    """Test basic DELETE query functionality"""

    def test_delete_from_table(self):
        """Test basic DELETE FROM table"""
        query = DELETE().FROM("users")
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "users"' in sql
        assert params == []

    def test_delete_with_where(self):
        """Test DELETE with WHERE clause"""
        query = DELETE().FROM("users").WHERE(col("id") == 1)
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "users"' in sql
        assert "WHERE" in sql
        assert "id = ?" in sql
        assert params == [1]

    def test_delete_with_multiple_conditions(self):
        """Test DELETE with multiple WHERE conditions"""
        age, active = cols("age", "active")
        query = DELETE().FROM("users").WHERE((age < 18) | (active == False))  # noqa: E712
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "users"' in sql
        assert "WHERE" in sql
        assert 18 in params
        assert False in params


@pytest.mark.delete
class TestDeleteAdvanced:
    """Test advanced DELETE query functionality"""

    def test_delete_with_complex_conditions(self):
        """Test DELETE with complex WHERE conditions"""
        age, salary, last_login = cols("age", "salary", "last_login")
        query = (
            DELETE()
            .FROM("employees")
            .WHERE(((age > 65) | (salary < 20000)) & (last_login < text("2020-01-01")))
        )
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "employees"' in sql
        assert "WHERE" in sql
        assert 65 in params
        assert 20000 in params
        assert "2020-01-01" in params

    def test_delete_with_and_conditions(self):
        """Test DELETE with AND conditions"""
        status, created_at = cols("status", "created_at")
        query = (
            DELETE()
            .FROM("logs")
            .WHERE((status == "processed") & (created_at < text("2023-01-01")))
        )
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "logs"' in sql
        assert "WHERE" in sql
        assert "processed" in params
        assert "2023-01-01" in params

    def test_delete_with_or_conditions(self):
        """Test DELETE with OR conditions"""
        status, expired = cols("status", "expired")
        query = (
            DELETE().FROM("sessions").WHERE((status == "invalid") | (expired == True))  # noqa: E712
        )
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "sessions"' in sql
        assert "WHERE" in sql
        assert "invalid" in params
        assert True in params

    def test_delete_with_numeric_comparison(self):
        """Test DELETE with numeric comparison"""
        score = col("score")
        query = DELETE().FROM("test_results").WHERE(score < 50)
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "test_results"' in sql
        assert "WHERE" in sql
        assert 50 in params

    def test_delete_with_string_comparison(self):
        """Test DELETE with string comparison"""
        category = col("category")
        query = DELETE().FROM("products").WHERE(category == "discontinued")
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "products"' in sql
        assert "WHERE" in sql
        assert "discontinued" in params

    def test_delete_with_null_check(self):
        # no longer unsupported
        """Test DELETE with NULL check"""
        query = DELETE().FROM("users").WHERE(col("last_login") == None)  # noqa: E711
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "users"' in sql
        assert "WHERE" in sql
        assert "IS NULL" in sql

    def test_delete_with_not_equal(self):
        """Test DELETE with not equal condition"""
        status = col("status")
        query = DELETE().FROM("orders").WHERE(status != "completed")
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "orders"' in sql
        assert "WHERE" in sql
        assert "completed" in params

    def test_delete_with_greater_than(self):
        """Test DELETE with greater than condition"""
        age = col("age")
        query = DELETE().FROM("users").WHERE(age > 100)
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "users"' in sql
        assert "WHERE" in sql
        assert 100 in params

    def test_delete_with_less_than_or_equal(self):
        """Test DELETE with less than or equal condition"""
        quantity = col("quantity")
        query = DELETE().FROM("inventory").WHERE(quantity <= 0)
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "inventory"' in sql
        assert "WHERE" in sql
        assert 0 in params

    def test_delete_with_datetime_expression(self):
        """Test DELETE with DATETIME expression"""
        signup_date, total_purchases, infractions = cols(
            "signup_date", "total_purchases", "infractions"
        )
        query = (
            DELETE()
            .FROM("customers")
            .WHERE(
                ((signup_date - col("CURRENT_TIMESTAMP")) > text("1 year").DATETIME())
                & (total_purchases > 1000)
                & (infractions == 0)
            )
        )
        sql, params = query.placeholder_pair()
        assert 'DELETE FROM "customers"' in sql
        assert "WHERE" in sql
        assert "DATETIME(?)" in sql
        assert "1 year" in params
        assert 1000 in params
        assert 0 in params
