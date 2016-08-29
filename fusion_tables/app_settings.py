from django.conf import settings


MODELS_TO_SYNC = getattr(settings, "MODELS_TO_SYNC")
CLIENT_SECRET_JSON_FILEPATH = getattr(settings, "CLIENT_SECRET_JSON_FILEPATH")
DELEGATED_CREDENTIALS = getattr(settings, "DELEGATED_CREDENTIALS", "")
DATETIME_FIELDS = getattr(settings, "DATETIME_FIELDS", (
    "DateField", "DatetimeField", "TimeField"))
LOCATION_FIELDS = getattr(settings, "LOCATION_FIELDS", ())
NUMBER_FIELDS = getattr(settings, "NUMBER_FIELDS", (
    "AutoField", "DecimalField", "FloatField", "IntegerField",
    "SmallIntegerField", "BigIntegerField", "PositiveIntegerField",
    "PositiveSmallIntegerField", "OneToOneField", "ForeignKey"))
