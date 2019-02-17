import requests
import json
from jinja2 import Template
import urllib.request
import tempfile


class GrafanaHelper(object):

    def __init__(self, grafana_server_address, grafana_token):
        self.grafana_token = grafana_token
        self.grafana_server_address = grafana_server_address

    def get_dashboards(self, tag=None):
        if tag is not None:
            result = self.call_grafana(
                "search?type=dash-db&tag={0}".format(tag))
        else:
            result = self.call_grafana("search?type=dash-db")
        return result

    def get_dashboard_details(self, slug):
        result = self.call_grafana("dashboards/db/{0}".format(slug))
        return result

    def search_dashboards(self, query):
        result = self.call_grafana(
            "search?type=dash-db&query={0}".format(query))
        return result

    def render(self, slug):
        timespan = {
            "from": "now-6h",
            "to": "now"
        }
        apiEndpoint = 'dashboard-solo'
        variables = ''
        template_params = []
        visualPanelId = False
        apiPanelId = False
        pname = False
        imagesize = {
            "width": 1000,
            "height": 500
        }
        parts = slug.split(":")
        if len(parts) > 1:
            slug = parts[0]
            if parts[1].isDigit():
                visualPanelId = int(parts[1])
            else:
                pname = parts[1].lower()

        dashboard = self.get_dashboard_details(slug)
        if not dashboard["dashboard"] or len(
            dashboard["dashboard"]["rows"]) == 0:
            return "Dashboard empty"
        data = dashboard["dashboard"]
        if len(data["templating"]["list"]) > 0:
            template_map = []
            for template in data["templating"]["list"]:
                if not "current" in template:
                    continue
                for _param in template_params:
                    if template.name == _param.name:
                        template_map["$" + template.name] = _param.value
                    else:
                        template_map[
                            "$" + template.name] = template.current.text
        panelNumber = 0
        for row in data["rows"]:
            for panel in row["panels"]:
                panelNumber += 1
            # Skip if visual panel ID was specified and didn't match
            if visualPanelId and apiPanelId != panel["id"]:
                continue
            # Skip if API panel ID was specified and didn't match
            if apiPanelId and apiPanelId != panel["id"]:
                continue

            if pname and panel["title"].lower().index(pname) == -1:
                continue

            title = self.formatTitleWithTemplate(panel["title"], template_map)
            #            imageUrl = "#{grafana_host}/render/#{apiEndpoint}/db/#{slug}/
            # ?panelId=#{panel.id}&width=#{imagesize.width}&height=#{imagesize.height}
            # &from=#{timespan.from}&to=#{timespan.to}#{variables}"
            imageUrl = "{0}/render/{1}/db/{2}/?panelId={3}&width={4}&height={5}&from={6}&to={7}{8}".format(
                self.grafana_server_address,
                apiEndpoint,
                slug,
                panel["id"],
                imagesize["width"],
                imagesize["height"],
                timespan["from"],
                timespan["to"],
                variables
            )

            link = "#{grafana_host}/dashboard/db/#{slug}/?panelId=#{panel.id}&fullscreen&from=#{timespan.from}&to=#{timespan.to}#{variables}"

            return {
                "imageUrl": imageUrl,
                "link": link
            }

    def formatTitleWithTemplate(self, title, template_map):
        # todo: format title
        return title

    def pretty_dashboards(self, response):
        with open('templates/grafana_dashboards_list.md') as file_:
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

    def get_grafana_image(self, url):
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ("Authorization", "Bearer {0}".format(self.grafana_token))
            ]
        urllib.request.install_opener(opener)
#        fd, path = tempfile.mkstemp()
        path, headers = urllib.request.urlretrieve(url)
        return {
            "path": path,
            "headers": headers
        }

    def grafana_headers(self, post=False):
        headers = {"Accept": "application/json",
                   "Authorization": "Bearer {0}".format(self.grafana_token)
                   }
        if post:
            headers["Content-Type"] = "application/json"
        return headers
