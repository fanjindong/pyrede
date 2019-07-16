.. pyrede documentation master file, created by
   sphinx-quickstart on Fri May 17 17:07:38 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyrede's documentation!
==================================


**Usage**

The rede is an effective 'snooze button' for events,
you push an event into it along (for future referance) and in how many seconds you want it back,
and poll whenever you want the elements back. only expired elements would pop out.


.. code-block:: python

   import pyrede
   import redis

   rede = pyrede.Rede(redis.Redis(decode_responses=True), "demo")

   rede.push("123", 1)
   rede.push("456", 1)
   rede.push("789", 3)

   time.sleep(1)

   list(rede.poll())

**Output:** ``["123", "456"]``


.. toctree::
   :maxdepth: 2

   pyrede/install
   pyrede/quickstart


The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
