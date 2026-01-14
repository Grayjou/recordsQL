"""Tests for COUNT queries"""
import pytest
from recordsql import COUNT, col, cols, text


@pytest.mark.count
class TestCountBasic:
    """Test basic COUNT query functionality"""

    def test_count_all(self):
        """Test COUNT(*) FROM table"""
        query = COUNT().FROM("users")
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert 'FROM "users"' in sql
        assert params == []

    def test_count_with_where(self):
        """Test COUNT with WHERE clause"""
        age = col("age")
        query = COUNT().FROM("users").WHERE(age > 18)
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert 'FROM "users"' in sql
        assert "WHERE" in sql
        assert params == [18]

    def test_count_with_multiple_conditions(self):
        """Test COUNT with multiple WHERE conditions"""
        age, active = cols("age", "active")
        query = COUNT().FROM("users").WHERE((age > 18) & (active == True))
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "WHERE" in sql
        assert 18 in params
        assert True in params


@pytest.mark.count
class TestCountAdvanced:
    """Test advanced COUNT query functionality"""

    def test_count_with_group_by(self):
        """Test COUNT with GROUP BY"""
        query = COUNT().FROM("employees").GROUP_BY("department")
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "GROUP BY department" in sql

    def test_count_with_having(self):
        """Test COUNT with HAVING clause"""
        salary = col("salary")
        query = COUNT().FROM("employees").GROUP_BY("department").HAVING(salary > 100000)
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "GROUP BY department" in sql
        assert "HAVING" in sql
        assert 100000 in params

    def test_count_with_complex_conditions(self):
        """Test COUNT with complex WHERE conditions"""
        age, salary, department = cols("age", "salary", "department")
        query = (
            COUNT()
            .FROM("employees")
            .WHERE(((age > 30) & (salary > 50000)) | (department == "Executive"))
        )
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "WHERE" in sql
        assert 30 in params
        assert 50000 in params
        assert "Executive" in params

    def test_count_with_datetime_expression(self):
        """Test COUNT with DATETIME expression"""
        signup_date, total_purchases, infractions = cols(
            "signup_date", "total_purchases", "infractions"
        )
        query = (
            COUNT()
            .FROM("customers")
            .WHERE(
                ((signup_date - col("CURRENT_TIMESTAMP")) > text("1 year").DATETIME())
                & (total_purchases > 1000)
                & (infractions == 0)
            )
        )
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "WHERE" in sql
        assert "DATETIME(?)" in sql
        assert "1 year" in params
        assert 1000 in params
        assert 0 in params

    def test_count_with_or_conditions(self):
        """Test COUNT with OR conditions"""
        status, verified = cols("status", "verified")
        query = COUNT().FROM("users").WHERE((status == "active") | (verified == True))
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "WHERE" in sql
        assert "active" in params
        assert True in params

    def test_count_with_not_equal(self):
        """Test COUNT with not equal condition"""
        status = col("status")
        query = COUNT().FROM("orders").WHERE(status != "cancelled")
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "WHERE" in sql
        assert "cancelled" in params

    def test_count_with_group_by_having(self):
        """Test COUNT with both GROUP BY and HAVING"""
        age, salary = cols("age", "salary")
        query = (
            COUNT()
            .FROM("employees")
            .WHERE(age > 25)
            .GROUP_BY("department")
            .HAVING(salary > 50000)
        )
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "WHERE" in sql
        assert "GROUP BY department" in sql
        assert "HAVING" in sql
        assert 25 in params
        assert 50000 in params

    def test_count_specific_column(self):
        """Test COUNT on specific column (if supported)"""
        query = COUNT("id").FROM("users")
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT" in sql
        assert 'FROM "users"' in sql

    def test_count_with_string_comparison(self):
        """Test COUNT with string comparison"""
        category = col("category")
        query = COUNT().FROM("products").WHERE(category == "Electronics")
        sql, params = query.placeholder_pair()
        assert "SELECT COUNT(*)" in sql
        assert "WHERE" in sql
        assert "Electronics" in params
