import os
import pprint
from datetime import datetime, timedelta

from errbot import Message, webhook, arg_botcmd
from errbot import botcmd, BotPlugin
from grafanahelper import GrafanaHelper


def get_ts():
    now = datetime.now()
    return '%s.%d' % (now.strftime('%Y%m%d-%H%M%S'), now.microsecond)


class SaGrafana(BotPlugin):

    def get_configuration_template(self):
        return {'server_address': 'https://host/grafana',
                'token': 'eyJrIjoicmNveFpac0tBZm81YzFrMDRNdWVQelRaN3VEOG5tblMiLCJuIjoiZS1ncmFmYW5hIiwiaWQiOjF9'}

    @botcmd(template="grafana_dashboards_list")
    def grafana_dashboards_list(self, mess, args):
        """List of dashboards"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        result = helper.get_dashboards()
        return {'dashboards': result}

    @botcmd(template="grafana_dashboards_list")
    @arg_botcmd('tag', type=str)  # bytag
    def grafana_dashboards_bytag(self, mess, tag):
        """List of dashboards by tag"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        self.log.info("sagrafana:  Getting dashboards for tag %s" % tag)
        result = helper.get_dashboards(tag=tag)
        return {'dashboards': result}

    @botcmd(template="grafana_dashboards_list")
    @arg_botcmd('query', type=str)  # bytag
    def grafana_dashboards_query(self, mess, query):
        """Fuzzy find dashboard by string"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        result = helper.search_dashboards(query=query)
        return {'dashboards': result}

    # @botcmd(template="grafana_debug")
    # def grafana_dashboard(self, mess, args):
    #     """Fuzzy find dashboard by string"""
    #     helper = GrafanaHelper(
    #         grafana_server_address=self.config['server_address'],
    #         grafana_token=self.config['token'])
    #     result = helper.get_dashboard_details(slug=mess)
    #     return {'result': result}

    @botcmd
    def grafana_render(self, mess, args):
        """Renders panel to slack"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        graphic = helper.render("aws-ec2")
        image_pack = helper.get_grafana_image(graphic["imageUrl"])
        stream = self.send_stream_request(mess.frm, open(image_pack["path"], 'rb'), name='render.png', stream_type='image/png')

    @botcmd
    def grafana_status(self, mess, args):
        """Check aliveness of solution"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        try:
            result = helper.get_dashboards()
            return "Seems alive - {0} dashboards found {1}".format(len(result),
                                                                   result)
        except Exception as err:
            return "Oops: {0}".format(err)
