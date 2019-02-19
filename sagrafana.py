import os
import re
from datetime import datetime
from errbot import arg_botcmd, botcmd, BotPlugin
from grafanahelper import GrafanaHelper


def get_ts():
    now = datetime.now()
    return '%s.%d' % (now.strftime('%Y%m%d-%H%M%S'), now.microsecond)


class SaGrafana(BotPlugin):

    def get_configuration_template(self):
        return {'server_address': 'https://host/grafana',
                'token': 'eyJrIjoicmNveFpac0tBZm81YzFrMDRNdWVQelRaN3VEOG5tblMiLCJuIjoiZS1ncmFmYW5hIiwiaWQiOjF9'}

    @botcmd(template='grafana_dashboards_list')
    def grafana_dashboards_list(self, mess, args):
        """List of dashboards"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        result = helper.get_dashboards()
        return {'dashboards': result}

    @arg_botcmd('tag', type=str, template='grafana_dashboards_list')  # bytag
    def grafana_dashboards_bytag(self, mess, tag):
        """List of dashboards by tag"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        self.log.info("sagrafana:  Getting dashboards for tag %s" % tag)
        result = helper.get_dashboards(tag=tag)
        return {'dashboards': result}

    @arg_botcmd('query', type=str, template='grafana_dashboards_list')  # bytag
    def grafana_dashboards_query(self, mess, query):
        """Fuzzy find dashboard by string"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        result = helper.search_dashboards(query=query)
        return {'dashboards': result}

    @arg_botcmd('slug', type=str,
                template='grafana_dashboard_details')  # byslug
    def grafana_dashboard(self, mess, slug):
        """Dashboard details"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        self.log.info("Getting %s dashboard details" % slug)
        result = helper.get_dashboard_details(slug)
        return {
            'dashboard': result,
            'slug': slug
        }

    @arg_botcmd('target', type=str)
    @arg_botcmd('--from', dest='start', type=str)
    @arg_botcmd('--to', dest='finish', type=str,
                template="grafana_render_panel")
    def grafana_render(self, target, start, finish, args):
        """Renders panel to slack"""
        helper = GrafanaHelper(
            grafana_server_address=self.config['server_address'],
            grafana_token=self.config['token'])
        self.log.info("Rendering with message %s" % mess)
        self.log.info("For period %s - %s" % (start, finish))

        regex = "([A-Za-z0-9\-\:_]+)(.*)?"
        matches = re.findall(regex, target)[0]
        slug = matches[0].strip()
        tuning_params = matches[1].strip()

        graphic = helper.render(
            period_from=start,
            period_finish=finish,
            slug=slug,
            tuning_params=tuning_params
        )
        image_pack = helper.get_grafana_image(graphic["imageUrl"])
        self.send_stream_request(mess.frm, open(image_pack["path"], 'rb'),
                                 name='render.png', stream_type='image/png')
        os.remove(image_pack["path"])

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
