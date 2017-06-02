from nose import SkipTest

from .base import TransportCase, redirect_stdouts


class TestDjango(TransportCase):
    """Djagno test case."""

    transport = 'django'
    prefix = 'django'
    event_loop_max = 10

    def before_connect(self):
        """Before connect."""

        @redirect_stdouts
        def setup_django(stdout, stderr):
            """Setup Django."""
            try:
                import django  # noqa
            except ImportError:
                raise SkipTest('django not installed')
            from django.conf import settings
            if not settings.configured:
                settings.configure(
                    DATABASE_ENGINE='sqlite3',
                    DATABASE_NAME=':memory:',
                    DATABASES={
                        'default': {
                            'ENGINE': 'django.db.backends.sqlite3',
                            'NAME': ':memory:',
                        },
                    },
                    INSTALLED_APPS=('djkombu', ),
                )
            from django.core.management import call_command
            call_command('migrate')

        setup_django()
