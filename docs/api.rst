API Reference
=============

This page provides detailed API documentation for all recordsQL classes and functions.

Query Builders
--------------

SELECT Query
~~~~~~~~~~~~

.. autoclass:: recordsQL.SelectQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsQL.SELECT

INSERT Query
~~~~~~~~~~~~

.. autoclass:: recordsQL.InsertQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsQL.INSERT

.. autoclass:: recordsQL.OnConflictQuery
   :members:
   :inherited-members:
   :special-members: __init__

UPDATE Query
~~~~~~~~~~~~

.. autoclass:: recordsQL.UpdateQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsQL.UPDATE

DELETE Query
~~~~~~~~~~~~

.. autoclass:: recordsQL.DeleteQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsQL.DELETE

COUNT Query
~~~~~~~~~~~

.. autoclass:: recordsQL.CountQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsQL.COUNT

EXISTS Query
~~~~~~~~~~~~

.. autoclass:: recordsQL.ExistsQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsQL.EXISTS

WITH Query (CTEs)
~~~~~~~~~~~~~~~~~

.. autoclass:: recordsQL.WithQuery
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: recordsQL.WITH

JOIN Query
~~~~~~~~~~

.. autoclass:: recordsQL.JoinQuery
   :members:
   :inherited-members:
   :special-members: __init__

Type Definitions
----------------

.. autoclass:: recordsQL.SQLCol
   :members:
   :inherited-members:

.. autoclass:: recordsQL.SQLInput
   :members:
   :inherited-members:

.. autoclass:: recordsQL.SQLOrderBy
   :members:
   :inherited-members:

Helper Functions
----------------

Column and Value Helpers
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: recordsQL.cols

.. autofunction:: recordsQL.col

.. autofunction:: recordsQL.text

.. autofunction:: recordsQL.num

.. autofunction:: recordsQL.set_expr

Base Classes
------------

RecordQuery
~~~~~~~~~~~

.. autoclass:: recordsQL.base.RecordQuery
   :members:
   :inherited-members:
   :special-members: __init__
