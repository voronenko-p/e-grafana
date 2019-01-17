import requests
import json
from jinja2 import Template


class GrafanaHelper(object):

  def __init__(self, grafana_server_address, grafana_token):
    self.grafana_token = grafana_token
    self.grafana_server_address = grafana_server_address

  def get_dashboards(self, tag=None):
    if tag is not None:
      result = self.call_grafana("search?type=dash-db&tag={0}".format(tag))
    else:
      result = self.call_grafana("search?type=dash-db")
    return result

  def get_dashboard_details(self, slug):
    result = self.call_grafana("dashboards/db/{0}".format(slug))
    return result

  def search_dashboards(self, query):
    result = self.call_grafana("search?type=dash-db&query={0}".format(query))
    return result

  def pretty_dashboards(self, response):
    with open('templates/grafana/grafana_dashboards_list.md') as file_:
      template = Template(file_.read())
      rendered = template.render(dashboards=response)
      return rendered

  def call_grafana(self, url):
    """

    :type url: basestring
    """
    target_url = "{0}/api/{1}".format(self.grafana_server_address, url)
    r = requests.get(target_url, headers=self.grafana_headers(False))
    result = json.loads(r.content)
    return result

  def post_grafana(self, url, data):
    target_url = "{0}/api/{1}".format(self.grafana_server_address, url)
    r = requests.post(target_url, data=json.dumps(data),
                      headers=self.grafana_headers(True))
    result = json.loads(r.content)
    return result

  def grafana_headers(self, post=False):
    headers = {"Accept": "application/json",
               "Authorization": "Bearer {0}".format(self.grafana_token)
               }
    if post:
      headers["Content-Type"] = "application/json"
    return headers
