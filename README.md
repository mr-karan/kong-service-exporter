<a href="https://zerodha.tech"><img src="https://zerodha.tech/static/images/github-badge.svg" align="right" /></a>

# Kong Service Registry Exporter

This is a small utility to export a Markdown file containing the list of services and other useful information from Kong's config.

If you're using Kong with [Declarative Configuration](https://docs.konghq.com/gateway-oss/2.3.x/db-less-and-declarative-config/), you'd know the config file can easily grow in 1000s of lines with 40-50 services. This utility aims to extract some of the useful information in a Markdown file and display as a table. 

## Usage

```
usage: main.py [-h] [--config CONFIG] [--output OUTPUT]

Generate Service Registry (markdown) using Kong config

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Path to Kong config file (YAML). (default: config-sample.yml)
  --output OUTPUT  Path to store the generated markdown file. (default: out.md)
```

### Quickstart

```
$ python3 main.py --config=config.yml --output=kong-service-registry.md
```

### Sample File

You can see the [generated](./kong_service_exporter/example/service_registry_sample.md) Markdown file from the [sample](./kong_service_exporter/example/config-sample.yml) config file.
