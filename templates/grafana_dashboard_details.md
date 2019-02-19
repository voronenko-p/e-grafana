id slug title *comma tags * 

{{ dashboard["id"] }} {{ dashboard["uri"]|replace('db/', '')}} {{ dashboard["title"] }} {% for tag in dashboard.tags %}*{{ tag }}*{% if not loop.last %},{% endif %}{% endfor %}

Possible params

{% for param in dashboard["templating"]["list] %}
  {{param["label"]}} {{param["name"]}}
{% endfor %}

Panels

number   id  title
{% for panel in dashboard["allpanels"] %}
{{ panel["panel_number"] }} {{ panel["id"] }} *{{panel["title"]}}*
_!grafana render {{ dashboard["uri"]|replace('db/', '')}}:{{panel["panel_number"] }}_

_!grafana render {{ dashboard["uri"]|replace('db/', '')}}:SUBSTRING_
{% endfor %}

{{ dashboard | tojson }}

