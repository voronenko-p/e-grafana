!repos install https://github.com/voronenko-p/e-grafana.git
!plugin config SaGrafana {'server_address': 'http://10.9.0.138/grafana', 'token': 'eyJrIjoicmNveFpac0tBZm81YzFrMDRNdWVQelRaN3VEOG5tblMiLCJuIjoiZS1ncmFmYW5hIiwiaWQiOjF9'}


Plugin features

`!grafana dashboards list`

```md

1 / 2Bv_gM4mk
AWS EC2 at /grafana/d/2Bv_gM4mk/aws-ec2
3 / sW0CVG4iz
Docker and system monitoring at /grafana/d/sW0CVG4iz/docker-and-system-monitoring
2 / xo1uVGViz
Docker Host & Container Overview at /grafana/d/xo1uVGViz/docker-host-and-container-overview

```

`*!grafana status*`

```md
Seems alive - 17 dashboards found
```

`!grafana dashboards bytag cloudwatch`

```
TODO
```

`!grafana dashboards query AWS`
