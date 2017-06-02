"""Kombu transport using the Django database as a message store."""
from __future__ import absolute_import

from anyjson import loads, dumps

from django.conf import settings
from django.core import exceptions as errors

from kombu.five import Empty
from kombu.transport import virtual
from kombu.utils import cached_property, symbol_by_name
from kombu.utils.encoding import bytes_to_str


VERSION = (2, 0, 0)

__author__ = "Ask Solem"
__contact__ = "ask@celeryproject.org"
__homepage__ = "http://github.com/celery/django-kombu/"
__docformat__ = "restructuredtext"
__license__ = "BSD"
__version__ = '.'.join(map(str, VERSION))

POLLING_INTERVAL = getattr(settings, 'KOMBU_POLLING_INTERVAL',
                           getattr(settings, 'DJKOMBU_POLLING_INTERVAL', 5.0))


class Channel(virtual.Channel):
    """Channel."""

    queue_model = 'djkombu.models:Queue'

    def _new_queue(self, queue, **kwargs):
        """New queue."""
        self.Queue.objects.get_or_create(name=queue)

    def _put(self, queue, message, **kwargs):
        """Put."""
        self.Queue.objects.publish(queue, dumps(message))

    def basic_consume(self, queue, *args, **kwargs):
        """Basic consume."""
        qinfo = self.state.bindings[queue]
        exchange = qinfo[0]
        if self.typeof(exchange).type == 'fanout':
            return
        super(Channel, self).basic_consume(queue, *args, **kwargs)

    def _get(self, queue):
        """Get."""
        m = self.Queue.objects.fetch(queue)
        if m:
            return loads(bytes_to_str(m))
        raise Empty()

    def _size(self, queue):
        """Size.

        :return: Number of items in the Queue
        :rtype: int
        """
        return self.Queue.objects.size(queue)

    def _purge(self, queue):
        """Purge.

        :return: Number of items removed.
        :rtype: int
        """
        return self.Queue.objects.purge(queue)

    def refresh_connection(self):
        """Refresh connection."""
        from django import db
        db.close_connection()

    @cached_property
    def Queue(self):
        """Queue model.

        :return: Queue model.
        :rtype: djkombu.models.Queue
        """
        return symbol_by_name(self.queue_model)


class Transport(virtual.Transport):
    """Transport."""

    Channel = Channel

    default_port = 0
    polling_interval = POLLING_INTERVAL
    channel_errors = (
        virtual.Transport.channel_errors + (
            errors.ObjectDoesNotExist, errors.MultipleObjectsReturned)
    )
    driver_type = 'sql'
    driver_name = 'django'

    def driver_version(self):
        """Driver version.

        :return: Django version.
        :rtype: str
        """
        import django
        return '.'.join(map(str, django.VERSION))
