Installation
============

Requirements
------------

- Python >= 3.8.1, < 4.0
- expressQL >= 0.2.4

Installing from PyPI
--------------------

The easiest way to install recordsQL is using pip:

.. code-block:: bash

   pip install expressQL
   pip install recordsQL

Installing from Source
----------------------

You can also install recordsQL from source:

.. code-block:: bash

   git clone https://github.com/Grayjou/recordsQL.git
   cd recordsQL
   pip install .

Development Installation
------------------------

If you want to contribute to recordsQL, install it in development mode with all dependencies:

.. code-block:: bash

   git clone https://github.com/Grayjou/recordsQL.git
   cd recordsQL
   poetry install

Verifying Installation
----------------------

To verify that recordsQL has been installed correctly, you can run:

.. code-block:: python

   import recordsQL
   print(recordsQL.__version__)
