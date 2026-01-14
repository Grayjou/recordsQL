API Reference
=============

This page provides detailed API documentation for all recordsql classes and functions.

Query Builders
--------------

SELECT Query
~~~~~~~~~~~~

.. autoclass:: recordsql.SelectQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsql.SELECT

INSERT Query
~~~~~~~~~~~~

.. autoclass:: recordsql.InsertQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsql.INSERT

.. autoclass:: recordsql.OnConflictQuery
   :members:
   :inherited-members:
   :special-members: __init__

UPDATE Query
~~~~~~~~~~~~

.. autoclass:: recordsql.UpdateQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsql.UPDATE

DELETE Query
~~~~~~~~~~~~

.. autoclass:: recordsql.DeleteQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsql.DELETE

COUNT Query
~~~~~~~~~~~

.. autoclass:: recordsql.CountQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsql.COUNT

EXISTS Query
~~~~~~~~~~~~

.. autoclass:: recordsql.ExistsQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsql.EXISTS

WITH Query (CTEs)
~~~~~~~~~~~~~~~~~

.. autoclass:: recordsql.WithQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsql.WITH

JOIN Query
~~~~~~~~~~

.. autoclass:: recordsql.JoinQuery
   :members:
   :inherited-members:
   :special-members: __init__

Type Definitions
----------------

.. autoclass:: recordsql.SQLCol
   :members:
   :inherited-members:

.. autoclass:: recordsql.SQLInput
   :members:
   :inherited-members:

.. autoclass:: recordsql.SQLOrderBy
   :members:
   :inherited-members:

Helper Functions
----------------

Column and Value Helpers
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: recordsql.cols

.. autofunction:: recordsql.col

.. autofunction:: recordsql.text

.. autofunction:: recordsql.num

.. autofunction:: recordsql.set_expr

Base Classes
------------

RecordQuery
~~~~~~~~~~~

.. autoclass:: recordsql.base.RecordQuery
   :members:
   :inherited-members:
   :special-members: __init__
