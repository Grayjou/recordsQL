"""Tests for JOIN operations"""
import pytest
from recordsql import SELECT, WITH, cols, col, num


@pytest.mark.join
class TestJoinBasic:
    """Test basic JOIN query functionality"""

    def test_inner_join(self):
        """Test INNER JOIN"""
        user_id, order_id = cols("user_id", "order_id")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert '"orders"' in sql
        assert "ON" in sql

    def test_left_join(self):
        """Test LEFT JOIN"""
        user_id = col("user_id")
        query = (
            SELECT()
            .FROM("users")
            .LEFT_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
        )
        sql, params = query.placeholder_pair()
        assert "LEFT JOIN" in sql
        assert '"orders"' in sql
        assert "ON" in sql

    def test_right_join(self):
        """Test RIGHT JOIN"""
        user_id = col("user_id")
        query = (
            SELECT()
            .FROM("users")
            .RIGHT_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
        )
        sql, params = query.placeholder_pair()
        assert "RIGHT JOIN" in sql
        assert '"orders"' in sql
        assert "ON" in sql

    def test_full_join(self):
        """Test FULL JOIN"""
        user_id = col("user_id")
        query = (
            SELECT()
            .FROM("users")
            .FULL_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
        )
        sql, params = query.placeholder_pair()
        assert "FULL JOIN" in sql or "FULL OUTER JOIN" in sql
        assert '"orders"' in sql
        assert "ON" in sql


@pytest.mark.join
class TestJoinAdvanced:
    """Test advanced JOIN query functionality"""

    def test_multiple_joins(self):
        """Test multiple JOIN operations"""
        user_id, order_id = cols("user_id", "order_id")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
            .LEFT_JOIN(table_name="payments", on=(order_id == col("payment_order_id")))
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert "LEFT JOIN" in sql
        assert '"orders"' in sql
        assert '"payments"' in sql

    def test_join_with_where(self):
        """Test JOIN with WHERE clause"""
        user_id, age = cols("user_id", "age")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
            .WHERE(age > 18)
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert "WHERE" in sql
        assert 18 in params

    def test_join_with_order_by(self):
        """Test JOIN with ORDER BY"""
        user_id, created_at = cols("user_id", "created_at")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
            .ORDER_BY(created_at, "DESC")
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert "ORDER BY created_at DESC" in sql

    def test_join_with_limit(self):
        """Test JOIN with LIMIT"""
        user_id = col("user_id")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
            .LIMIT(10)
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert "LIMIT 10" in sql

    def test_join_with_numeric_condition(self):
        """Test JOIN with numeric condition in ON clause"""
        store_id = num(1275682)
        query = (
            SELECT()
            .FROM("products")
            .INNER_JOIN(table_name="prices", on=(store_id == col("store_id")))
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert '"prices"' in sql
        assert 1275682 in params

    def test_with_query_and_joins(self):
        """Test WITH query with JOINs"""
        name, age, email, total_purchases = cols(
            "name", "age", "email", "total_purchases"
        )
        current_store_id = num(1275682)

        select_query = SELECT(name, age, email).FROM("users").WHERE(age > 18)

        with_query = (
            WITH(select_query.AS("adult_users"))
            .SELECT(name, age, email)
            .FROM("adult_users")
        )

        # Add JOINs
        with_query.INNER_JOIN(
            table_name="prices", on=(current_store_id == col("store_id"))
        ).LEFT_JOIN(table_name="orders", on=(current_store_id == col("store_id")))

        sql, params = with_query.placeholder_pair()
        assert "WITH adult_users AS" in sql
        assert "INNER JOIN" in sql
        assert "LEFT JOIN" in sql
        assert '"prices"' in sql
        assert '"orders"' in sql
        assert 1275682 in params

    def test_join_with_complex_where(self):
        """Test JOIN with complex WHERE conditions"""
        user_id, age, status = cols("user_id", "age", "status")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
            .WHERE((age > 18) & (status == "active"))
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert "WHERE" in sql
        assert 18 in params
        assert "active" in params

    def test_three_table_join(self):
        """Test JOIN across three tables"""
        user_id, order_id, product_id = cols("user_id", "order_id", "product_id")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
            .INNER_JOIN(
                table_name="products", on=(product_id == col("order_product_id"))
            )
        )
        sql, params = query.placeholder_pair()
        assert sql.count("INNER JOIN") == 2
        assert '"orders"' in sql
        assert '"products"' in sql

    def test_mixed_join_types(self):
        """Test mix of different JOIN types"""
        user_id, order_id, product_id = cols("user_id", "order_id", "product_id")
        query = (
            SELECT()
            .FROM("users")
            .INNER_JOIN(table_name="orders", on=(user_id == col("order_user_id")))
            .LEFT_JOIN(table_name="payments", on=(order_id == col("payment_order_id")))
            .RIGHT_JOIN(
                table_name="products", on=(product_id == col("order_product_id"))
            )
        )
        sql, params = query.placeholder_pair()
        assert "INNER JOIN" in sql
        assert "LEFT JOIN" in sql
        assert "RIGHT JOIN" in sql
