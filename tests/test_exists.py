"""Tests for EXISTS queries"""
import pytest
from recordsQL import EXISTS, col, cols, text


@pytest.mark.exists
class TestExistsBasic:
    """Test basic EXISTS query functionality"""

    def test_exists_basic(self):
        """Test basic EXISTS query"""
        query = EXISTS().FROM("users")
        sql, params = query.placeholder_pair()
        assert "SELECT EXISTS" in sql or "EXISTS" in sql
        assert '"users"' in sql
        assert params == []

    def test_exists_with_where(self):
        """Test EXISTS with WHERE clause"""
        age = col("age")
        query = EXISTS().FROM("users").WHERE(age > 18)
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert params == [18]

    def test_exists_with_multiple_conditions(self):
        """Test EXISTS with multiple WHERE conditions"""
        age, active = cols("age", "active")
        query = EXISTS().FROM("users").WHERE((age > 18) & (active == True))
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert 18 in params
        assert True in params


@pytest.mark.exists
class TestExistsAdvanced:
    """Test advanced EXISTS query functionality"""

    def test_exists_with_complex_conditions(self):
        """Test EXISTS with complex WHERE conditions"""
        age, salary, department = cols("age", "salary", "department")
        query = (
            EXISTS()
            .FROM("employees")
            .WHERE(((age > 30) & (salary > 50000)) | (department == "Executive"))
        )
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert 30 in params
        assert 50000 in params
        assert "Executive" in params

    def test_exists_with_datetime_expression(self):
        """Test EXISTS with DATETIME expression"""
        signup_date, total_purchases, infractions = cols(
            "signup_date", "total_purchases", "infractions"
        )
        query = (
            EXISTS()
            .FROM("customers")
            .WHERE(
                ((signup_date - col("CURRENT_TIMESTAMP")) > text("1 year").DATETIME())
                & (total_purchases > 1000)
                & (infractions == 0)
            )
        )
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert "DATETIME(?)" in sql
        assert "1 year" in params
        assert 1000 in params
        assert 0 in params

    def test_exists_with_or_conditions(self):
        """Test EXISTS with OR conditions"""
        status, verified = cols("status", "verified")
        query = EXISTS().FROM("users").WHERE((status == "active") | (verified == True))
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert "active" in params
        assert True in params

    def test_exists_with_and_conditions(self):
        """Test EXISTS with AND conditions"""
        age, department = cols("age", "department")
        query = (
            EXISTS().FROM("employees").WHERE((age > 40) & (department == "Management"))
        )
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert 40 in params
        assert "Management" in params

    def test_exists_with_not_equal(self):
        """Test EXISTS with not equal condition"""
        status = col("status")
        query = EXISTS().FROM("orders").WHERE(status != "cancelled")
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert "cancelled" in params

    def test_exists_with_string_comparison(self):
        """Test EXISTS with string comparison"""
        category = col("category")
        query = EXISTS().FROM("products").WHERE(category == "Electronics")
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert "Electronics" in params

    def test_exists_with_numeric_comparison(self):
        """Test EXISTS with numeric comparison"""
        price = col("price")
        query = EXISTS().FROM("products").WHERE(price > 100)
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert 100 in params

    def test_exists_with_null_check(self):
        """Test EXISTS with NULL check - skipped due to expressql limitation"""
        """No longer unsuported"""
        query = EXISTS().FROM("users").WHERE(col("last_login") == None)
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
    def test_exists_with_greater_than_or_equal(self):
        """Test EXISTS with greater than or equal condition"""
        score = col("score")
        query = EXISTS().FROM("test_results").WHERE(score >= 90)
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert 90 in params

    def test_exists_with_less_than(self):
        """Test EXISTS with less than condition"""
        quantity = col("quantity")
        query = EXISTS().FROM("inventory").WHERE(quantity < 10)
        sql, params = query.placeholder_pair()
        assert "EXISTS" in sql
        assert "WHERE" in sql
        assert 10 in params
