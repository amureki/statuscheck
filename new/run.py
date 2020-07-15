import sys
from new.__about__ import __url__
from new.check import get_statuscheck_api

import click


@click.command()
@click.argument("service")
def main(service):
    try:
        service_api = get_statuscheck_api(service)
    except ModuleNotFoundError:
        click.echo(f'"{service}" is not implemented, leave a note at {__url__}')
        return 1

    _print_status(service_api)

    return 0


def _print_status(service_api):
    summary = service_api.get_summary()
    click.echo(f"Current {service_api.name} status: {summary.status.description}")

    incidents = summary.incidents
    if incidents:
        click.echo(f"Registered events:")
        for incident in incidents:
            if hasattr(incident, "status"):
                click.echo(f"- [{incident.status}] {incident.name}")
            else:
                click.echo(f"- {incident.name}")
            if hasattr(incident, "scheduled_for"):
                click.echo(f"  {incident.scheduled_for}")
            # TODO: verbosity 2?
            if incident.components:
                click.echo(f"  Affected components:")
                for component in incident.components:
                    click.echo(f"    - {component.name} [{component.status}]")

    # TODO: if status not OK?
    if incidents:
        click.echo()
        click.echo(f"More: {service_api.status_url}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
