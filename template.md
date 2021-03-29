# Kong Service Registry

Last updated at {{updated_at}}.


| Name | Route  | Upstream  | ACL Group  |
|---|---|---|---|
{% for svc in services -%}
|  {{svc.name}} | {{svc.routes}}  | {{svc.endpoint}} | {{svc.acls}} |
{% endfor %}
