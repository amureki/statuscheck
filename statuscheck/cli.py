import sys
import click

from .__about__ import __url__
from statuscheck.check import get_statuscheck_api
from statuscheck.exceptions import StatusCheckParsingError


@click.command()
@click.argument('service')
def main(service):
    """Console script for statuscheck."""
    try:
        service_api = get_statuscheck_api(service)
    except ModuleNotFoundError:
        click.echo(f'"{service}" is not implemented, leave a note at {__url__}')
        return 1
    try:
        summary = service_api.get_summary()
    except StatusCheckParsingError as e:
        click.echo(str(e))
        return 1

    status = summary.status
    incidents = summary.incidents
    has_components = hasattr(summary, 'components')

    click.echo(f'{service_api.name}')
    if incidents:
        incident = incidents[0]['name']
        click.echo(f'{status}: {incident}')
    else:
        click.echo(f'{status}')
    if has_components and summary.components:
        click.echo(f'Affected components:')
        for component in summary.components:
            name = component['name']
            status = component['status']
            click.echo(f'{name}: {status}')
    if incidents or (has_components and summary.components):
        click.echo(f'More: {service_api.status_url}')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
