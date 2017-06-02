"""Kombu transport using the Django database as a message store."""


default_app_config = 'djkombu.apps.KombuAppConfig'

VERSION = (2, 0, 0)

__author__ = "Ask Solem"
__contact__ = "ask@celeryproject.org"
__homepage__ = "http://github.com/celery/django-kombu/"
__docformat__ = "restructuredtext"
__license__ = "BSD"
__version__ = '.'.join(map(str, VERSION))

from kombu.transport import TRANSPORT_ALIASES

TRANSPORT_ALIASES.update({
    'django': 'djkombu.transport.Transport'
})
