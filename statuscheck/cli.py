import sys

import click

from statuscheck.check import get_statuscheck_api

from .__about__ import __url__


@click.command()
@click.argument("service")
def main(service):
    """Console script for statuscheck."""
    try:
        service_api = get_statuscheck_api(service)
    except ModuleNotFoundError:
        click.echo(f'"{service}" is not implemented, leave a note at {__url__}')
        return 1

    summary = service_api.get_summary()

    click.echo(f"Current status of {service_api.name}: {summary.status}")

    incidents = summary.incidents
    if incidents:
        click.echo(f"Registered incidents:")
        for incident in incidents:
            incident_name = incident["name"]
            incident_status = incident.get("status")
            if incident_status:
                click.echo(f"- {incident_name} [{incident_status}]")
            else:
                click.echo(f"- {incident_name}")

    has_components = hasattr(summary, "components")
    if has_components and summary.components:
        click.echo(f"Affected components:")
        for component in summary.components:
            name = component["name"]
            component_status = component["status"]
            click.echo(f"- {name}: {component_status}")

    if incidents or (has_components and summary.components):
        click.echo()
        click.echo(f"More: {service_api.status_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
