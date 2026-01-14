"""Tests for WITH (CTE) queries"""
import pytest
from recordsql import WITH, SELECT, cols, col, text


@pytest.mark.with_query
class TestWithBasic:
    """Test basic WITH (CTE) query functionality"""

    def test_with_simple_cte(self):
        """Test simple WITH clause"""
        name, age = cols("name", "age")
        inner_query = SELECT(name, age).FROM("users").WHERE(age > 18)

        with_query = WITH(inner_query.AS("adults")).SELECT(name).FROM("adults")
        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "adults AS" in sql
        assert "SELECT" in sql
        assert 18 in params

    def test_with_cte_and_where(self):
        """Test WITH clause with additional WHERE in main query"""
        name, age, city = cols("name", "age", "city")
        inner_query = SELECT(name, age, city).FROM("users").WHERE(age > 18)

        with_query = (
            WITH(inner_query.AS("adults"))
            .SELECT(name)
            .FROM("adults")
            .WHERE(city == "New York")
        )
        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "adults AS" in sql
        assert "WHERE" in sql
        assert 18 in params
        assert "New York" in params


@pytest.mark.with_query
class TestWithAdvanced:
    """Test advanced WITH (CTE) query functionality"""

    def test_with_complex_cte(self):
        """Test WITH clause with complex query"""
        name, age, email, total_purchases, signup_date, infractions = cols(
            "name", "age", "email", "total_purchases", "signup_date", "infractions"
        )

        select_query = (
            SELECT(name, age, email, total_purchases)
            .FROM("customers")
            .WHERE(
                ((signup_date - col("CURRENT_TIMESTAMP")) > text("1 year").DATETIME())
                & (total_purchases > 1000)
                & (infractions == 0)
            )
            .ORDER_BY(total_purchases, "DESC")
            .LIMIT(10)
            .OFFSET(1)
        )

        with_query = (
            WITH(select_query.AS("customer_data"))
            .SELECT(name, age, email, total_purchases)
            .FROM("customer_data")
            .WHERE((total_purchases > 1000) & (infractions == 0))
            .ORDER_BY(total_purchases, "DESC")
            .LIMIT(10)
            .OFFSET(1)
        )

        sql, params = with_query.placeholder_pair()
        assert "WITH customer_data AS" in sql
        assert "SELECT" in sql
        assert 'FROM "customer_data"' in sql or "FROM customer_data" in sql
        assert "1 year" in params
        assert 1000 in params
        assert 0 in params

    def test_with_order_by_limit_offset(self):
        """Test WITH clause with ORDER BY, LIMIT, and OFFSET"""
        name, created_at = cols("name", "created_at")
        inner_query = (
            SELECT(name, created_at)
            .FROM("users")
            .ORDER_BY(created_at, "DESC")
            .LIMIT(100)
        )

        with_query = (
            WITH(inner_query.AS("recent_users"))
            .SELECT(name)
            .FROM("recent_users")
            .LIMIT(10)
            .OFFSET(5)
        )

        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "recent_users AS" in sql
        assert "LIMIT" in sql

    def test_with_and_group_by(self):
        """Test WITH clause with GROUP BY"""
        salary = col("salary")
        inner_query = (
            SELECT("department", "salary").FROM("employees").WHERE(salary > 50000)
        )

        with_query = (
            WITH(inner_query.AS("high_earners"))
            .SELECT("department")
            .FROM("high_earners")
            .GROUP_BY("department")
        )

        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "high_earners AS" in sql
        assert "GROUP BY department" in sql
        assert 50000 in params

    def test_with_multiple_conditions(self):
        """Test WITH clause with multiple conditions"""
        age, status, verified = cols("age", "status", "verified")
        inner_query = (
            SELECT("name", "age", "status")
            .FROM("users")
            .WHERE((age > 18) & (status == "active") & (verified == True))
        )

        with_query = (
            WITH(inner_query.AS("active_users"))
            .SELECT("name", "age")
            .FROM("active_users")
            .WHERE(age < 65)
        )

        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "active_users AS" in sql
        assert 18 in params
        assert "active" in params
        assert True in params
        assert 65 in params

    def test_with_and_having(self):
        """Test WITH clause with HAVING"""
        count = col("count")
        inner_query = SELECT("department").FROM("employees")

        with_query = (
            WITH(inner_query.AS("dept_data"))
            .SELECT("department")
            .FROM("dept_data")
            .GROUP_BY("department")
            .HAVING(count > 10)
        )

        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "dept_data AS" in sql
        assert "GROUP BY department" in sql
        assert "HAVING" in sql
        assert 10 in params

    def test_with_numeric_operations(self):
        """Test WITH clause with numeric operations"""
        price, discount, quantity = cols("price", "discount", "quantity")
        inner_query = (
            SELECT(price, discount, quantity)
            .FROM("products")
            .WHERE((price - discount) > 50)
        )

        with_query = (
            WITH(inner_query.AS("discounted_products"))
            .SELECT(price, discount)
            .FROM("discounted_products")
            .WHERE(quantity > 0)
        )

        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "discounted_products AS" in sql
        assert 50 in params
        assert 0 in params

    def test_with_string_comparison(self):
        """Test WITH clause with string comparison"""
        name, category, status = cols("name", "category", "status")
        inner_query = (
            SELECT(name, category).FROM("products").WHERE(category == "Electronics")
        )

        with_query = (
            WITH(inner_query.AS("electronics"))
            .SELECT(name)
            .FROM("electronics")
            .WHERE(status == "available")
        )

        sql, params = with_query.placeholder_pair()
        assert "WITH" in sql
        assert "electronics AS" in sql
        assert "Electronics" in params
        assert "available" in params
