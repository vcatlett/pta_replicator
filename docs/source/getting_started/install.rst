*****************************
Installing ``pta_replicator``
*****************************

TODO: Actually put it on PyPi lol

``pta_replicator`` requires Python 3.10+ and recent versions of
`astropy <https://astropy.org>`_,
`numpy <https://numpy.org>`_,
`scipy <https://scipy.org>`_,
`pandas <https://pandas.pydata.org>`_,
`matplotlib <https://matplotlib.org>`_.

With ``pip`` from PyPi
======================

``pta_replicator`` is most easily installed with ``pip``, which will take care of
any dependencies. Within a virtual environment, run

.. code::

    (your-venv) $ pip install pta_replicator


From GitHub
===========

To install from GitHub within a given environment:

.. code::

    (your-venv) $ git clone git@github.com:vcatlett/pta_replicator.git
    (your-venv) $ cd pta_replicator
    (your-venv) $ pip install -e .
