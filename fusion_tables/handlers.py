"""fusion_tables handlers."""

import django.apps
from django.db.models import signals
from django.dispatch import receiver

from . import app_settings
from . import sync


def push_data(sender, instance, **kwargs):
    """Post save receiver."""
    return sync.push_data(instance)


@receiver(signals.post_migrate)
def sync_model(sender, app_config, **kwargs):
    """Push django model data to google fusion table."""
    for model_string in app_settings.MODELS_TO_SYNC:
        model_class = django.apps.apps.get_model(model_string)
        signals.post_save.connect(push_data, sender=model_class)
