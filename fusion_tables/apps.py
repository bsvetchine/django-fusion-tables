"""fusion_tables app configuration file."""

from django.apps import AppConfig


class FusionTablesConfig(AppConfig):
    """Tandoori PDF app config."""

    name = "fusion_tables"

    def ready(self):
        """Connect signals."""
        from . import handlers  # NOQA
