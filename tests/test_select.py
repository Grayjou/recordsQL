"""Tests for SELECT queries"""
import pytest
from recordsQL import SELECT, cols, col, text, num


@pytest.mark.select
class TestSelectBasic:
    """Test basic SELECT query functionality"""

    def test_select_all(self):
        """Test SELECT * FROM table"""
        query = SELECT().FROM("users")
        sql, params = query.placeholder_pair()
        assert 'SELECT *' in sql
        assert '"users"' in sql
        assert params == []

    def test_select_specific_columns(self):
        """Test SELECT with specific columns"""
        query = SELECT("name", "age", "email").FROM("users")
        sql, params = query.placeholder_pair()
        assert 'SELECT name, age, email' in sql
        assert '"users"' in sql
        assert params == []

    def test_select_with_where(self):
        """Test SELECT with WHERE clause"""
        age = col("age")
        query = SELECT("name", "age").FROM("users").WHERE(age > 18)
        sql, params = query.placeholder_pair()
        assert 'SELECT name, age' in sql
        assert 'WHERE' in sql
        assert 'age > ?' in sql
        assert params == [18]

    def test_select_with_multiple_conditions(self):
        """Test SELECT with multiple WHERE conditions"""
        age, active = cols("age", "active")
        query = SELECT("name").FROM("users").WHERE((age > 18) & (active == True))
        sql, params = query.placeholder_pair()
        assert 'WHERE' in sql
        assert '?' in sql
        assert 18 in params
        assert True in params

    def test_select_with_order_by(self):
        """Test SELECT with ORDER BY"""
        query = SELECT("name", "age").FROM("users").ORDER_BY("age", "DESC")
        sql, params = query.placeholder_pair()
        assert 'ORDER BY age DESC' in sql

    def test_select_with_limit(self):
        """Test SELECT with LIMIT"""
        query = SELECT().FROM("users").LIMIT(10)
        sql, params = query.placeholder_pair()
        assert 'LIMIT 10' in sql

    def test_select_with_offset(self):
        """Test SELECT with OFFSET"""
        query = SELECT().FROM("users").LIMIT(10).OFFSET(5)
        sql, params = query.placeholder_pair()
        assert 'LIMIT 10' in sql
        assert 'OFFSET 5' in sql


@pytest.mark.select
class TestSelectAdvanced:
    """Test advanced SELECT query functionality"""

    def test_select_with_limit_offset_order(self):
        """Test SELECT with ORDER BY, LIMIT, and OFFSET"""
        query = (
            SELECT("name", "created_at")
            .FROM("users")
            .ORDER_BY("created_at", "DESC")
            .LIMIT(10)
            .OFFSET(20)
        )
        sql, params = query.placeholder_pair()
        assert 'ORDER BY created_at DESC' in sql
        assert 'LIMIT 10' in sql
        assert 'OFFSET 20' in sql

    def test_select_with_complex_conditions(self):
        """Test SELECT with complex WHERE conditions"""
        age, salary = cols("age", "salary")
        query = SELECT("name").FROM("employees").WHERE(
            ((age > 25) & (age < 50)) & (salary > 50000)
        )
        sql, params = query.placeholder_pair()
        assert 'WHERE' in sql
        assert 25 in params
        assert 50 in params
        assert 50000 in params

    def test_select_with_or_conditions(self):
        """Test SELECT with OR conditions"""
        age, department = cols("age", "department")
        query = SELECT("name").FROM("employees").WHERE(
            (age > 60) | (department == "Executive")
        )
        sql, params = query.placeholder_pair()
        assert 'WHERE' in sql
        assert 60 in params
        assert "Executive" in params

    def test_select_with_group_by(self):
        """Test SELECT with GROUP BY"""
        query = SELECT("department").FROM("employees").GROUP_BY("department")
        sql, params = query.placeholder_pair()
        assert 'GROUP BY department' in sql

    def test_select_with_having(self):
        """Test SELECT with HAVING clause"""
        salary = col("salary")
        query = (
            SELECT("department")
            .FROM("employees")
            .GROUP_BY("department")
            .HAVING(salary > 100000)
        )
        sql, params = query.placeholder_pair()
        assert 'GROUP BY department' in sql
        assert 'HAVING' in sql
        assert 100000 in params

    def test_select_expression_in_where(self):
        """Test SELECT with expression in WHERE clause"""
        price, discount = cols("price", "discount")
        query = SELECT().FROM("products").WHERE((price - discount) > 50)
        sql, params = query.placeholder_pair()
        assert 'WHERE' in sql
        assert '-' in sql
        assert 50 in params

    def test_select_with_text_function(self):
        """Test SELECT with text() function"""
        signup_date, total_purchases = cols("signup_date", "total_purchases")
        query = SELECT().FROM("customers").WHERE(
            ((signup_date - col("CURRENT_TIMESTAMP")) > text("1 year").DATETIME())
            & (total_purchases > 1000)
        )
        sql, params = query.placeholder_pair()
        assert 'WHERE' in sql
        assert 'DATETIME(?)' in sql
        assert '1 year' in params
        assert 1000 in params

    def test_select_with_num(self):
        """Test SELECT with num() function"""
        price = col("price")
        # Note: num() rounds to integer
        threshold = num(99)
        query = SELECT().FROM("products").WHERE(price > threshold)
        sql, params = query.placeholder_pair()
        assert 'WHERE' in sql
        assert 99 in params
