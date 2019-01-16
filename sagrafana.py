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
  @arg_botcmd('filter_tag', type=str)
  def grafana_dashboards(self, filter_tag=None):
    """List of dashboards with optional tag"""
    helper = GrafanaHelper(grafana_server_address=self.config['server_address'],
                           grafana_token=self.config['token'])
    result = helper.get_dashboards(tag=filter_tag)
    return {'dashboards': result}

  @botcmd
  def status(self):
    """Say hello to the world"""
    helper = GrafanaHelper(grafana_server_address=self.config['server_address'],
                           grafana_token=self.config['token'])
    try:
        result = helper.get_dashboards()
        return "Seems alive - {0} dashboards found".format(len(result))
    except Exception as err:
        return "Oops: {0}".format(err)
