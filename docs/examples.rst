Advanced Examples
=================

This page demonstrates advanced usage patterns and features of recordsql.

Complex SELECT Queries
----------------------

Using ORDER BY, LIMIT, and OFFSET
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import SELECT, cols, col

   name, age, email = cols("name", "age", "email")

   query = SELECT(name, age, email).FROM("users").WHERE(
       age > 18
   ).ORDER_BY(
       age, "DESC"
   ).LIMIT(10).OFFSET(5)

   sql, params = query.placeholder_pair()
   print(sql)
   # Output: SELECT name, age, email FROM "users" WHERE age > ? ORDER BY age DESC LIMIT 10 OFFSET 5

Multiple ORDER BY Clauses
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import SELECT, cols

   name, age, created_at = cols("name", "age", "created_at")

   query = SELECT(name, age).FROM("users").ORDER_BY(
       age, "DESC",
       (created_at, "ASC")
   )

   sql, params = query.placeholder_pair()
   print(sql)
   # Output: SELECT name, age FROM "users" ORDER BY age DESC, created_at ASC

Working with JOINs
------------------

INNER JOIN Example
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import SELECT, cols, col

   name, email, order_id = cols("name", "email", "order_id")

   query = SELECT(name, email, order_id).FROM("users").INNER_JOIN(
       table_name="orders",
       on=(col("users.id") == col("orders.user_id"))
   )

   sql, params = query.placeholder_pair()
   print(sql)
   # Output: SELECT name, email, order_id FROM "users" INNER JOIN "orders" ON users.id = orders.user_id

Multiple JOINs
~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import SELECT, cols, col

   name, product_name, quantity = cols("name", "product_name", "quantity")

   query = SELECT(name, product_name, quantity).FROM("users")
   query.INNER_JOIN(
       table_name="orders",
       on=(col("users.id") == col("orders.user_id"))
   ).LEFT_JOIN(
       table_name="products",
       on=(col("orders.product_id") == col("products.id"))
   )

   sql, params = query.placeholder_pair()
   print(sql)

Common Table Expressions (CTEs)
--------------------------------

Basic WITH Query
~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import WITH, SELECT, cols

   name, age = cols("name", "age")

   # First, create a SELECT query
   inner_query = SELECT(name, age).FROM("users").WHERE(age > 18)

   # Then wrap it in a WITH query
   query = WITH(inner_query.AS("adults")).SELECT(name, age).FROM("adults")

   sql, params = query.placeholder_pair()
   print(sql)
   # Output: WITH adults AS (SELECT name, age FROM "users" WHERE age > ?) SELECT name, age FROM "adults"

WITH Query with JOINs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import WITH, SELECT, cols, col, num

   name, age, email, total_purchases = cols("name", "age", "email", "total_purchases")
   store_id = num(12345)

   # Create the CTE
   inner_query = SELECT(name, age, email, total_purchases).FROM("customers").WHERE(
       total_purchases > 1000
   )

   # Create the main query with JOIN
   # Join on the store_id column from the stores table
   current_store_id = num(12345)
   
   query = WITH(inner_query.AS("high_value_customers")).SELECT(
       name, age, email
   ).FROM("high_value_customers").INNER_JOIN(
       table_name="stores",
       on=(current_store_id == col("store_id"))
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)

INSERT with ON CONFLICT
-----------------------

Upsert Pattern (PostgreSQL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import INSERT, col

   query = INSERT("user_id", "name", "email").INTO("users").VALUES(
       (1, "John Doe", "john@example.com")
   ).ON_CONFLICT(
       do="UPDATE",
       conflict_cols=["user_id"],
       set={"name": "John Doe Updated", "email": "john.updated@example.com"}
   ).RETURNING("user_id", "name", "email")

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)

INSERT with WHERE Condition on Conflict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import INSERT, col

   query = INSERT("user_id", "status").INTO("users").VALUES(
       (1, "active")
   ).ON_CONFLICT(
       do="UPDATE",
       conflict_cols=["user_id"],
       set={"status": "active"},
       where=col("status") == "inactive"
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)

Complex WHERE Conditions
------------------------

Using Logical Operators
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import SELECT, cols, col, text

   name, age, status, created_at = cols("name", "age", "status", "created_at")

   query = SELECT(name, age).FROM("users").WHERE(
       ((age >= 18) & (age <= 65)) &
       ((status == "active") | (status == "pending")) &
       ((created_at - col("CURRENT_TIMESTAMP")) > text("1 year").DATETIME())
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)

Using DATETIME Functions
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import SELECT, cols, col, text

   name, signup_date = cols("name", "signup_date")

   query = SELECT(name).FROM("users").WHERE(
       (signup_date - col("CURRENT_TIMESTAMP")) > text("30 days").DATETIME()
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)

Aggregation Queries
-------------------

Using GROUP BY and HAVING
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import COUNT, cols

   user_id, total_purchases = cols("user_id", "total_purchases")

   query = COUNT().FROM("orders").GROUP_BY(user_id).HAVING(
       total_purchases > 10
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)

EXISTS Queries
--------------

Checking for Record Existence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import EXISTS, col

   query = EXISTS().FROM("users").WHERE(
       (col("email") == "john@example.com") &
       (col("status") == "active")
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)
   # Output: SELECT EXISTS(SELECT 1 FROM "users" WHERE (email = ?) AND (status = ?))
   # ['john@example.com', 'active']

UPDATE with RETURNING
---------------------

Getting Updated Values
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsql import UPDATE, col

   query = UPDATE("users").SET(
       name="John Doe",
       age=31,
       updated_at=col("CURRENT_TIMESTAMP")
   ).WHERE(
       col("user_id") == 123
   ).RETURNING("user_id", "name", "age", "updated_at")

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)
