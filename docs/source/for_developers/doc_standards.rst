*************
Documentation
*************

Sphinx Autobuilds on `novus`
============================

Here are the steps to set up Sphinx autobuilds so that you can check your documentation edits live.

1. First, navigate to your ``pta_replicator`` root directory and activate your environment. For example,

.. code-block:: bash

    $ conda activate pta_replicator-3.10

2. Next, tell `sphinx` to build the docs

.. code-block:: bash

    (pta_replicator-3.10) $ sphinx-autobuild docs/source docs/_build/html --host 127.0.1 --port 8000

3. In a separate shell, log into `novus` with

.. code-block:: bash

    $ ssh -L 8000:localhost:8000 {{USERNAME}}@novus.dri.oregonstate.edu

4. Navigate to `http://localhost:8000/` in your local browser

You may now make changes in the `pta_replicator/docs/` directory and see the live changes in your browser. To close the server, simply `CTRL+C`.

Docstring Format
================

All Python functions must contain a docstring which follows the NumPy convention. You can learn more about this convention here: https://numpydoc.readthedocs.io/en/latest/format.html

Mermaid Diagrams
================

Diagrams can be directly in these text files by using the `sphinxcontrib-mermaid` package. Here's an example:

.. mermaid::

    flowchart LR
        A[Item 1] --> B[Item 2]
        B --> C[Item 3]

To learn more, see the `package documentation <https://sphinxcontrib-mermaid-demo.readthedocs.io/en/latest/>`_. Mermaid also offers an `online editor <https://mermaid.live>`_ which can be used to design diagrams.
