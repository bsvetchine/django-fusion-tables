"""fusion_tables models."""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class FusionTable(models.Model):
    """"Link table between django model and fusion table."""
    # Django model
    django_model = models.ForeignKey(ContentType, unique=True)
    # Google fusion table id
    table_id = models.CharField(max_length=50, primary_key=True)

    class Meta:
        unique_together = (('django_model', 'table_id'), )


class FusionRow(models.Model):
    """Link table between django model instance and fusion table row."""
    # Django instance
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Google fusion row id
    row_id = models.PositiveIntegerField(primary_key=True)

    class Meta:
        unique_together = (
            ('content_type', 'object_id'),
            ('content_type', 'object_id', 'row_id'),
        )
