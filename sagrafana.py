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
  def grafana_dashboards(self, mess, args):
    """List of dashboards"""
    helper = GrafanaHelper(grafana_server_address=self.config['server_address'],
                           grafana_token=self.config['token'])
    result = helper.get_dashboards()
    return {'dashboards': result}

  @botcmd(template="grafana_dashboards_list")
  def grafana_dashboards_bytag(self, mess, args):
    """List of dashboards by tag"""
    helper = GrafanaHelper(grafana_server_address=self.config['server_address'],
                           grafana_token=self.config['token'])
    result = helper.get_dashboards(tag=mess)
    return {'dashboards': result}

  @botcmd(template="grafana_dashboards_list")
  def grafana_dashboards_query(self, mess, args):
    """Fuzzy find dashboard by string"""
    helper = GrafanaHelper(grafana_server_address=self.config['server_address'],
                           grafana_token=self.config['token'])
    result = helper.search_dashboards(query=mess)
    return {'dashboards': result}

  @botcmd(template="grafana_debug")
  def grafana_dashboard(self, mess, args):
    """Fuzzy find dashboard by string"""
    helper = GrafanaHelper(grafana_server_address=self.config['server_address'],
                           grafana_token=self.config['token'])
    result = helper.get_dashboard_details(slug=mess)
    return {'result': result}

  @botcmd
  def grafana_status(self, mess, args):
    """Check aliveness of solution"""
    helper = GrafanaHelper(grafana_server_address=self.config['server_address'],
                           grafana_token=self.config['token'])
    try:
        result = helper.get_dashboards()
        return "Seems alive - {0} dashboards found {1}".format(len(result), result)
    except Exception as err:
        return "Oops: {0}".format(err)
