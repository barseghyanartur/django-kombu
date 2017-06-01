============
django-kombu
============
Kombu transport using the Django database. Enables you to use the Django
database as the message store for `Kombu`_.

This package
:version: 2.0.0

Installation
============

(1) Install ``django-kombu``:

    .. code-block:: sh

        pip install django-kombu

(2) Add ``djkombu`` to ``INSTALLED_APPS``:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            'djkombu',
            # ...
        )

(3) Run migrations:

    .. code-block:: sh

        python manage.py migrate

Usage
=====

``django-kombu`` contains a single transport, ``djkombu.transport.Transport``,
which is used like this:

.. code-block:: python

    from kombu.connection import BrokerConnection
    c = BrokerConnection(transport="djkombu.transport.Transport")


.. _`Kombu`: http://pypi.python.org/pypi/kombu


License
=======

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
