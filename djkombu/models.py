from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import QueueManager, MessageManager


class Queue(models.Model):
    """Queue model."""

    name = models.CharField(_('name'), max_length=200, unique=True)

    objects = QueueManager()

    class Meta(object):
        """Meta options."""

        db_table = 'djkombu_queue'
        verbose_name = _('Queue')
        verbose_name_plural = _('Queues')


class Message(models.Model):
    """Message model."""

    visible = models.BooleanField(default=True, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True, db_index=True,
                                   auto_now_add=True)
    payload = models.TextField(_('payload'), null=False)
    queue = models.ForeignKey(Queue, related_name='messages')

    objects = MessageManager()

    class Meta(object):
        """Meta options."""

        db_table = 'djkombu_message'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
