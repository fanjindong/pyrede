.. _quickstart:

Quickstart
==========

.. image:: http://

.. module:: pyrede.core

Eager to get started? This page gives a good introduction in how to get started
with Pyrede.

First, make sure that:

* Pyrede is :ref:`installed <install>`


Let's get started with some simple examples.


Make a Rede
--------------

Making a rede with Pyrede is very simple.

Begin by importing the Pyrede module and create a redis instance.

.. code-block:: python

    import pyrede
    import redis

    rede = pyrede.Rede(redis.Redis(decode_responses=True), "demo") # Set the collection of elements to demo


PUSH
------

Push an ``element`` into the ``demo`` for ``ttl`` seconds.

    >>> rede.push("a", 1)


PULL
------

Pull the element corresponding with ``element`` and remove it from the ``demo`` rede before it expires.

    >>> rede.pull("a")


POLL
------

Pull and return all the expired elements in ``demo``.

    >>> rede.push("a", 1)
    >>> rede.push("b", 1)
    >>> rede.push("c", 3)

    >>> time.sleep(1)

    >>> rede.poll()
    ["a", "b"]

***Return Value***

List of all expired elements on success, or an empty list if no elements are expired, the key is empty or the key contains something other the a dehydrator.


LOOK
------

Show the element corresponding and without removing it from the dehydrator.

    >>> rede.push("a", 1)
    >>> rede.look("a")
    1

TTN
----

Show the time left (in seconds) until the next element will expire.

.. code-block:: python

    rede.push("a", 1)
    rede.push("b", 2)
    rede.push("c", 3)

>>> rede.ttn()
1

***Return Value***

int representing the number of seconds until next element will expire.
