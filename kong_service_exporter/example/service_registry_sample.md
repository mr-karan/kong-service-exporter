# Kong Service Registry

_Last updated at **2021-03-30 12:15:03**._

## Services

| Name | Route  | Upstream  | ACL Group  |
|---|---|---|---|
|  My-Awesome-SVC | `/my/api`  | http://mysvc-endpoint.internal:80/ | `mysvc-consumers` |


## Consumers

| User | ACL Group  |
|---|---|
|  myapp | `mysvc-consumers`, `anothersvc-consumers` |
