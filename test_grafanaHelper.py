from unittest import TestCase
from grafanahelper import GrafanaHelper

GRAFANA_ENDPOINT="http://10.9.0.138/grafana/"
GRAFANA_TOKEN="eyJrIjoicmNveFpac0tBZm81YzFrMDRNdWVQelRaN3VEOG5tblMiLCJuIjoiZS1ncmFmYW5hIiwiaWQiOjF9"

class TestGrafanaHelper(TestCase):
  def test_get_dashboards(self):
    grafanaHelper = GrafanaHelper(grafana_server_address=GRAFANA_ENDPOINT, grafana_token=GRAFANA_TOKEN)
    dashboards = grafanaHelper.get_dashboards()
    self.assertTrue(len(dashboards) >= 0)
    dashboards_md = grafanaHelper.pretty_dashboards(dashboards)
    self.assertIsNotNone(dashboards_md)
