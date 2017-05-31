"""Kombu transport using the Django database as a message store."""

try:
    from django.apps import AppConfig
except ImportError:  # pragma: no cover
    pass
else:
    class KombuAppConfig(AppConfig):
        name = 'djkombu.transport'
        label = name.replace('.', '_')
        verbose_name = 'Message queue'

    default_app_config = 'djkombu.KombuAppConfig'

VERSION = (2, 0, 0)

__author__ = "Ask Solem"
__contact__ = "ask@celeryproject.org"
__homepage__ = "http://github.com/celery/django-kombu/"
__docformat__ = "restructuredtext"
__license__ = "BSD"
__version__ = '.'.join(map(str, VERSION))
