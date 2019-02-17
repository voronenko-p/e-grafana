from unittest import TestCase
from grafanahelper import GrafanaHelper
import urllib.request

GRAFANA_ENDPOINT="http://10.9.0.138/grafana/"
GRAFANA_TOKEN="eyJrIjoicmNveFpac0tBZm81YzFrMDRNdWVQelRaN3VEOG5tblMiLCJuIjoiZS1ncmFmYW5hIiwiaWQiOjF9"

class TestGrafanaHelper(TestCase):
  def test_get_dashboards(self):
    grafanaHelper = GrafanaHelper(grafana_server_address=GRAFANA_ENDPOINT, grafana_token=GRAFANA_TOKEN)
    dashboards = grafanaHelper.get_dashboards()
    self.assertTrue(len(dashboards) >= 0)

  def test_get_dashboards_by_tag(self):
      grafanaHelper = GrafanaHelper(grafana_server_address=GRAFANA_ENDPOINT, grafana_token=GRAFANA_TOKEN)
      dashboards = grafanaHelper.get_dashboards(tag="cloudwatch")
      self.assertTrue(len(dashboards) >= 0)

  def test_grafana_dashboards_search(self):
    grafanaHelper = GrafanaHelper(grafana_server_address=GRAFANA_ENDPOINT, grafana_token=GRAFANA_TOKEN)
    dashboards = grafanaHelper.search_dashboards("aws")
    self.assertTrue(len(dashboards) >= 0)

  def test_pretty_dashboards(self):
    grafanaHelper = GrafanaHelper(grafana_server_address=GRAFANA_ENDPOINT, grafana_token=GRAFANA_TOKEN)
    dashboards = grafanaHelper.get_dashboards()
    self.assertTrue(len(dashboards) >= 0)
    dashboards_md = grafanaHelper.pretty_dashboards(dashboards)
    self.assertIsNotNone(dashboards_md)

  def test_get_dashboard_details(self):
    grafanaHelper = GrafanaHelper(grafana_server_address=GRAFANA_ENDPOINT, grafana_token=GRAFANA_TOKEN)
    dashboard = grafanaHelper.get_dashboard_details("aws-ec2")
    self.assertTrue(dashboard is not None)

  def test_render(self):
      grafanaHelper = GrafanaHelper(grafana_server_address=GRAFANA_ENDPOINT, grafana_token=GRAFANA_TOKEN)
      graphic = grafanaHelper.render("aws-ec2")
      self.assertTrue("imageUrl" in graphic)
      self.assertTrue("link" in graphic)
      image_pack = grafanaHelper.get_grafana_image(graphic["imageUrl"])
      # image/png
      self.assertTrue(image_pack["path"] != "")
