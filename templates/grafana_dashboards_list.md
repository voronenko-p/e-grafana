{% for dashboard in dashboards %}

{{ dashboard["id"] }} {{ dashboard["title"] }} {% for tag in dashboard.tags %}*{{ tag }}*{% if not loop.last %},{% endif %}{% endfor %}

_!grafana dashboard {{ dashboard["uri"]|replace('db/', '')}}_


{% endfor %}
