from __future__ import absolute_import

from functools import wraps

from django.db import connections, router, transaction, connection, models


try:
    transaction.atomic
except AttributeError:
    commit_on_success = transaction.commit_on_success
else:
    def commit_on_success(fun):
        """Commit on success.

        :param fun:
        """
        @wraps(fun)
        def _commit(*args, **kwargs):
            with transaction.atomic():
                return fun(*args, **kwargs)
        return _commit


class QueueManager(models.Manager):
    """Queue manger."""

    def publish(self, queue_name, payload):
        """Publish.

        :param queue_name:
        :param payload:
        """
        queue, created = self.get_or_create(name=queue_name)
        queue.messages.create(payload=payload)

    def fetch(self, queue_name):
        """Fetch.

        :param queue_name:
        :return: Queue instance
        :rtype: djkombu.models.Queue
        """
        try:
            queue = self.get(name=queue_name)
        except self.model.DoesNotExist:
            return

        return queue.messages.pop()

    def size(self, queue_name):
        """Size.

        :param queue_name:
        :return: Number of messages in the queue
        :rtype: int
        """
        return self.get(name=queue_name).messages.count()

    def purge(self, queue_name):
        """Purge.

        :param queue_name:
        :return: Number of messages removed
        :rtype: int
        """
        try:
            queue = self.get(name=queue_name)
        except self.model.DoesNotExist:
            return

        messages = queue.messages.all()
        count = messages.count()
        messages.delete()
        return count


def select_for_update(qs):
    """Select for update.

    :param qs:
    :return:
    """
    if connection.vendor == 'oracle':
        return qs
    try:
        return qs.select_for_update()
    except AttributeError:
        return qs


class MessageManager(models.Manager):
    """Message manager."""

    _messages_received = [0]
    cleanup_every = 10

    @commit_on_success
    def pop(self):
        """Pop.

        :return: Result payload.
        :rtype: str
        """
        try:
            resultset = select_for_update(
                self.filter(visible=True).order_by('sent_at', 'id')
            )
            result = resultset[0:1].get()
            result.visible = False
            result.save()
            recv = self.__class__._messages_received
            recv[0] += 1
            if not recv[0] % self.cleanup_every:
                self.cleanup()
            return result.payload
        except self.model.DoesNotExist:
            pass

    def cleanup(self):
        """Clean up."""
        cursor = self.connection_for_write().cursor()
        cursor.execute(
            'DELETE FROM %s WHERE visible=%%s' % (
                self.model._meta.db_table, ),
            (False, )
        )

    def connection_for_write(self):
        """Connection for write.

        :return: Connection
        """
        if connections:
            return connections[router.db_for_write(self.model)]
        return connection
