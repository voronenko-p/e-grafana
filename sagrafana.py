import os
import pprint
from datetime import datetime, timedelta

from errbot import Message, webhook
from errbot import botcmd, BotPlugin
from grafanahelper import GrafanaHelper

def get_ts():
  now = datetime.now()
  return '%s.%d' % (now.strftime('%Y%m%d-%H%M%S'), now.microsecond)

class SaGrafana(BotPlugin):

  def get_configuration_template(self):
    return {'server_address': 'https://host/grafana',
            'token':'eyJrIjoicmNveFpac0tBZm81YzFrMDRNdWVQelRaN3VEOG5tblMiLCJuIjoiZS1ncmFmYW5hIiwiaWQiOjF9'}

  @botcmd(template="grafana_dashboards_list")
  def grafana_dashboards(self, msg, args):
    helper= GrafanaHelper(grafana_server_address=self.config['server_address'], grafana_token=self.config['token'])

