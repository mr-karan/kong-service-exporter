# Kong Service Registry

_Last updated at **{{updated_at}}**._

## Services

| Name | Route  | Upstream  | ACL Group  |
|---|---|---|---|
{% for svc in services -%}
|  {{svc.name}} | {{svc.routes}}  | {{svc.endpoint}} | {{svc.acls}} |
{% endfor %}

## Consumers

| User | ACL Group  |
|---|---|
{% for cons in consumers -%}
|  {{cons.name}} | {{cons.groups}} |
{% endfor %}
