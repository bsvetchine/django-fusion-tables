# coding: utf-8
from django.test import TestCase

from . import models as test_models
from .. import models
from .. import tools


class FusionTableTestCase(TestCase):

    def setUp(self):
        self.service = tools.get_service()

    def check_google_fusion_table_format(self, table_id):
        response = self.service.table().get(
            tableId=table_id).execute()
        self.assertEqual(response[u'isExportable'], True)
        self.assertEqual(response[u'kind'], u'fusiontables#table')
        self.assertEqual(response[u'name'], u'fusion_tables_samplemodel')
        self.assertEqual(len(response[u'columns']), 6)
        col_def = {}
        for col in response[u'columns']:
            col_def[col[u'name']] = col[u'type']
        expected_col_def = {
            u'text': u'LOCATION', u'datetime': u'STRING', u'char': u'STRING',
            u'date': u'DATETIME', u'integer': u'NUMBER', u'id': u'NUMBER'}
        self.assertEqual(col_def, expected_col_def)

    def check_google_fusion_table_data(self, table_id, expected_data):
        select_query = "SELECT * FROM {table_id};".format(table_id=table_id)
        response = self.service.query().sql(sql=select_query).execute()
        self.assertEqual(response[u'kind'], u'fusiontables#sqlresponse')
        expected_col = [u'id', u'date', u'integer', u'datetime', u'text',
                        u'char']
        self.assertEqual(response[u'columns'], expected_col)
        self.assertEqual(response[u'rows'], expected_data)

    def test_post_save(self):
        self.assertEqual(test_models.SampleModel.objects.count(), 0)
        self.assertEqual(models.FusionTable.objects.count(), 0)
        self.assertEqual(models.FusionRow.objects.count(), 0)

        test_models.SampleModel.objects.create(
            date="2014-04-01", integer=35,
            datetime="2016-10-30T09:25:43.324809",
            text="Kraftwerkstrasse 7, 4133 Pratteln, Suisse",
            char="Z7, Pratteln")

        self.assertEqual(test_models.SampleModel.objects.count(), 1)
        self.assertEqual(models.FusionTable.objects.count(), 1)
        self.assertEqual(models.FusionRow.objects.count(), 1)

        fusion_table = models.FusionTable.objects.get()

        self.check_google_fusion_table_format(table_id=fusion_table.table_id)
        expected_data = [
            [u'1', u'2014-04-01', u'35', u'2016-10-30T09:25:43.324809',
             u'Kraftwerkstrasse 7, 4133 Pratteln, Suisse', u'Z7, Pratteln']]
        self.check_google_fusion_table_data(
            fusion_table.table_id, expected_data)

        test_models.SampleModel.objects.create(
            date="2015-02-19", integer=31,
            datetime="2018-1-30T09:25:43.324809",
            text=u"Parc de la Villette, 211 Avenue Jean Jaurès, 75019 Paris",
            char="Le Trabendo")

        self.assertEqual(test_models.SampleModel.objects.count(), 2)
        self.assertEqual(models.FusionTable.objects.count(), 1)
        self.assertEqual(models.FusionRow.objects.count(), 2)

        self.check_google_fusion_table_format(table_id=fusion_table.table_id)
        created_item = [
            u'2', u'2015-02-19', u'31', u'2018-1-30T09:25:43.324809',
            u'Parc de la Villette, 211 Avenue Jean Jaurès, 75019 Paris',
            u'Le Trabendo']
        expected_data.append(created_item)
        self.check_google_fusion_table_data(
            fusion_table.table_id, expected_data)
