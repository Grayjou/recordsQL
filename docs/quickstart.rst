Quick Start Guide
=================

This guide will help you get started with recordsQL quickly.

Basic Concepts
--------------

recordsQL provides a fluent, chainable API for building SQL queries. Each query builder returns an object that you can chain methods on to build complex queries.

Key Functions
~~~~~~~~~~~~~

- ``SELECT()``: Build SELECT queries
- ``INSERT()``: Build INSERT queries
- ``UPDATE()``: Build UPDATE queries
- ``DELETE()``: Build DELETE queries
- ``COUNT()``: Build COUNT queries
- ``EXISTS()``: Build EXISTS queries
- ``WITH()``: Build Common Table Expressions (CTEs)

Helper Functions
~~~~~~~~~~~~~~~~

- ``cols()``: Define multiple columns at once
- ``col()``: Reference a column
- ``text()``: Create a text literal
- ``num()``: Create a numeric literal
- ``set_expr()``: Create a SET expression

Your First Query
----------------

Building a Simple SELECT Query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsQL import SELECT, cols

   # Define columns
   name, age, email = cols("name", "age", "email")

   # Build a SELECT query
   query = SELECT(name, age, email).FROM("users")

   # Get SQL and parameters
   sql, params = query.placeholder_pair()
   print(sql)
   # Output: SELECT name, age, email FROM "users"

Adding WHERE Clauses
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsQL import SELECT, cols, col

   name, age = cols("name", "age")

   # Build a SELECT query with WHERE clause
   query = SELECT(name, age).FROM("users").WHERE(
       (age > 18) & (col("status") == "active")
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)
   # Output: SELECT name, age FROM "users" WHERE (age > ?) AND (status = ?)
   # [18, 'active']

Building an INSERT Query
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsQL import INSERT

   # Build an INSERT query
   query = INSERT("name", "age", "email").INTO("users").VALUES(
       ("John Doe", 30, "john@example.com"),
       ("Jane Smith", 25, "jane@example.com")
   )

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)

Building an UPDATE Query
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsQL import UPDATE, col

   # Build an UPDATE query
   query = UPDATE("users").SET(
       name="John Doe",
       age=31
   ).WHERE(col("user_id") == 123)

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)
   # Output: UPDATE "users" SET name = ?, age = ? WHERE user_id = ?
   # ['John Doe', 31, 123]

Building a DELETE Query
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from recordsQL import DELETE, col

   # Build a DELETE query
   query = DELETE().FROM("users").WHERE(col("user_id") == 123)

   sql, params = query.placeholder_pair()
   print(sql)
   print(params)
   # Output: DELETE FROM "users" WHERE user_id = ?
   # [123]

Next Steps
----------

- Check out the :doc:`examples` page for more advanced usage examples
- Explore the :doc:`api` reference for complete documentation
- Visit the `GitHub repository <https://github.com/Grayjou/recordsQL>`_ to contribute or report issues
