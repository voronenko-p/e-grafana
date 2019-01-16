{% for dashboard in dashboards %}

{{ dashboard["id"] }} / {{ dashboard["uid"] }}

{{ dashboard["title"] }} at {{ dashboard["url"] }}

{% for tag in tags %} *{{ tag }}*   {% endfor %} 

{% endfor %}