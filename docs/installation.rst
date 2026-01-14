Installation
============

Requirements
------------

- Python >= 3.8.1, < 4.0
- expressQL >= 0.2.4

Installing from PyPI
--------------------

The easiest way to install recordsql is using pip:

.. code-block:: bash

   pip install expressQL
   pip install recordsql

.. note::
   If recordsql is not yet published to PyPI, please install from source (see below).

Installing from Source
----------------------

You can also install recordsql from source:

.. code-block:: bash

   git clone https://github.com/Grayjou/recordsql.git
   cd recordsql
   pip install .

Development Installation
------------------------

If you want to contribute to recordsql, install it in development mode with all dependencies:

.. code-block:: bash

   git clone https://github.com/Grayjou/recordsql.git
   cd recordsql
   poetry install

Verifying Installation
----------------------

To verify that recordsql has been installed correctly, you can run:

.. code-block:: python

   import recordsql
   print(recordsql.__version__)
