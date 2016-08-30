"""
Model definition used for testing purposes only.

The following model definition are only used to generate a migration applied
on test database only.
"""

from django.db import models


class SampleModel(models.Model):
    """"Testing model."""
    date = models.DateField()
    integer = models.PositiveSmallIntegerField()
    datetime = models.DateTimeField()
    text = models.TextField()
    char = models.CharField(max_length=50)
