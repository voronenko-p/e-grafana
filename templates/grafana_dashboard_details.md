**id**  **slug**       **title**        *comma separated tags*

{{ dashboard["id"] }} {{ slug }} {{ dashboard["title"] }} {% for tag in dashboard.tags %}*{{ tag }}*{% if not loop.last %},{% endif %}{% endfor %}

Possible params

name label
{% for param in dashboard["templating"]["list"] %}
**{{param["name"]}}** _{{param["label"]}}_
{% endfor %}


Panels

**number**     id     title
{% for panel in dashboard["allpanels"] %}
**{{ panel["id"] }}**   "{{panel["title"]}}"

_!grafana render {{ slug }}:{{panel["id"] }}_ PARAM=VALUE from=now-6h to=now

_!grafana render {{ slug }}:TITLEQUERY_  PARAM=VALUE from=now-6h to=now
{% endfor %}
