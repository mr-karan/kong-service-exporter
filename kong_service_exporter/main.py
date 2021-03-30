import argparse
import sys
from datetime import datetime

import yaml
from jinja2 import Template

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


def get_consumer_groups(acls):
    """
    Given a list of plugins, filter out the `acl` plugin
    and return a formatted string
    of all the acl consumer group names which are `allowed`
    to access the service.
    """
    if acls is None:
        return
    return "`" + "`, `".join(i.get("group") for i in acls) + "`"


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

    consumers = []
    for i in data["consumers"]:
        consumers.append(
            {
                "name": i.get("username"),
                "groups": get_consumer_groups(i.get("acls")),
            }
        )

    md = tmpl.render(
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        services=sorted(services, key=lambda i: i["name"]),
        consumers=sorted(consumers, key=lambda i: i["name"]),
    )
    # save to disk.
    with open(output, "w", encoding="utf-8") as f:
        f.write(md)


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
        sys.exit(e)

    tmpl = load_template(TEMPLATE_FILE)
    render_template(data, tmpl, args.output)


if __name__ == "__main__":
    sys.exit(main())
