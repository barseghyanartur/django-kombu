try:
    from django.apps import AppConfig
except ImportError:  # pragma: no cover
    pass
else:
    class KombuAppConfig(AppConfig):
        """Kombu app config."""

        name = 'djkombu.transport'
        label = name.replace('.', '_')
        verbose_name = 'Message queue'
