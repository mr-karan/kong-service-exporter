import argparse
import logging
import sys
from datetime import datetime

import yaml
from jinja2 import Template

logger = logging.getLogger("kong_svc_reg_exporter")
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

TEMPLATE_FILE = "template.md"


def read_config(path):
    """
    Reads the Kong config file (YAML).
    """
    if path is None:
        raise Exception(
            "empty path provided. please provide a path using `--config=<config.yml>`"
        )
    with open(path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc


def load_template(tmpl):
    """
    Loads the default template file.
    """
    with open(tmpl, "r") as stream:
        return Template(stream.read())


def get_endpoint(svc):
    """
    Given a service object, return a formatted
    URL of the service.
    """
    return f"{svc.get('protocol')}://{svc.get('host')}:{svc.get('port','80')}{svc.get('path','/')}"


def get_routes(routes):
    """
    Given a list of routes, return a formatted string
    of all the routes.
    """
    return "`" + "`, `".join(p for r in routes for p in r["paths"]) + "`"


def get_acls(plugins):
    """
    Given a list of plugins, filter out the `acl` plugin
    and return a formatted string
    of all the acl consumer group names which are `allowed`
    to access the service.
    """
    if plugins is None:
        return
    for i in plugins:
        if i["name"] == "acl":
            return "`" + "`, `".join(a for a in i.get("config").get("allow")) + "`"


def render_template(data, tmpl, output):
    """
    Given the Kong config (`data`), and the template file object
    it renders the template and saves the file to disk.
    """

    services = []
    for i in data["services"]:
        services.append(
            {
                "name": i.get("name"),
                "endpoint": get_endpoint(i),
                "routes": get_routes(i.get("routes")),
                "acls": get_acls(i.get("plugins")),
            }
        )

    html = tmpl.render(
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), services=services
    )

    # save to disk.
    with open(f"{output}", "w", encoding="utf-8") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Service Registry (markdown) " + "using Kong config",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        action="store",
        default="config-sample.yml",
        help="Path to Kong config file (YAML).",
    )
    parser.add_argument(
        "--output",
        action="store",
        default="service_registry.md",
        help="Path to store the generated markdown file.",
    )
    args = parser.parse_args()

    try:
        data = read_config(args.config)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

    tmpl = load_template(TEMPLATE_FILE)
    render_template(data, tmpl, args.output)


if __name__ == "__main__":
    sys.exit(main())
