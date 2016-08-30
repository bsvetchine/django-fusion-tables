from django.contrib.contenttypes.models import ContentType

from . import app_settings
from . import models
from . import tools


class FusionTable(object):
    """Fusion table that reprepsents django model."""

    def __init__(self, model):
        """Get or create FusionTable instance from django model."""
        self.model = model
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        self.django_ct = ContentType.objects.get(
            app_label=app_label, model=model_name)

    def get_table_name(self):
        """Return fusion table corresponding to model."""
        return self.model._meta.db_table

    def get_column_type(self, field_type):
        """Return google fusion table column type from django field type."""
        if field_type in app_settings.DATETIME_FIELDS:
            return "DATETIME"
        if field_type in app_settings.LOCATION_FIELDS:
            return "LOCATION"
        if field_type in app_settings.NUMBER_FIELDS:
            return "NUMBER"
        return "STRING"

    def get_table_columns(self):
        """Return dict descr of model db columns."""
        columns = []
        for field in self.model._meta.get_fields():
            if field.concrete:
                columns.append({
                    "name": field.name,
                    "type": self.get_column_type(field.get_internal_type())
                })
        return columns

    def create(self):
        """Create fusion table for model."""
        service = tools.get_service()
        request = service.table().insert(body={
            "name": self.get_table_name(),
            "isExportable": True,
            "columns": self.get_table_columns()
        })
        response = request.execute()
        return models.FusionTable.objects.create(
            django_model=self.django_ct, table_id=response["tableId"])

    def get_or_create(self):
        try:
            table = models.FusionTable.objects.get(django_model=self.django_ct)
        except models.FusionTable.DoesNotExist:
            table = self.create()
        return table


class FusionRow(object):

    def __init__(self, instance):
        """Get or create FusionRow instance from django instance."""
        self.instance = instance
        self.table = FusionTable(self.instance.__class__)
        self.django_table = self.table.get_or_create()

    def get_sql_query(self):
        table_id = self.django_table.table_id
        columns = [column["name"] for column in self.table.get_table_columns()]
        values = u""
        for column in columns:
            values += u"'{value}', ".format(
                value=getattr(self.instance, column))
        values = values[:-2]
        return (
            u"INSERT INTO {table_id} ({columns}) VALUES ({values});".format(
                table_id=table_id, columns=", ".join(columns),
                values=values))

    def create(self):
        """Create a row into table."""
        service = tools.get_service()
        sql_query = self.get_sql_query()
        request = service.query().sql(sql=sql_query)
        response = request.execute()
        return models.FusionRow.objects.create(
            content_object=self.instance, row_id=response["rows"][0][0])

    def get_or_create(self):
        try:
            row = models.FusionRow.objects.get(
                content_type=self.table.django_ct,
                object_id=self.instance.pk)
        except models.FusionRow.DoesNotExist:
            row = self.create()
        return row


def push_data(instance):
    """Push django model data into google fusion table."""
    return FusionRow(instance).get_or_create()
