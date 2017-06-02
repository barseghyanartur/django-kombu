from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from six import python_2_unicode_compatible

from .managers import QueueManager, MessageManager


@python_2_unicode_compatible
class Queue(models.Model):
    """Queue model."""

    name = models.CharField(_('Name'), max_length=200, unique=True)

    objects = QueueManager()

    class Meta(object):
        """Meta options."""

        app_label = 'djkombu'
        db_table = 'djkombu_queue'
        verbose_name = _('Queue')
        verbose_name_plural = _('Queues')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
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

        app_label = 'djkombu'
        db_table = 'djkombu_message'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.payload
