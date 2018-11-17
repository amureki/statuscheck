import sys
import click

from .__about__ import __url__
from statuscheck.check import get_statuscheck_api
from statuscheck.exceptions import StatusCheckMissingArgumentsError, StatusCheckParsingError
from statuscheck.status_types import TYPE_GOOD, TYPE_UNKNOWN, TYPE_INCIDENT, TYPE_OUTAGE, \
    TYPE_MAINTENANCE

COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_DEFAULT = '\033[99m'

STATUSES_COLORS_MAPPING = {
    TYPE_UNKNOWN: COLOR_DEFAULT,
    TYPE_GOOD: COLOR_GREEN,
    TYPE_INCIDENT: COLOR_YELLOW,
    TYPE_OUTAGE: COLOR_RED,
    TYPE_MAINTENANCE: COLOR_DEFAULT,
}


@click.command()
@click.argument('service')
@click.option('--extra', '-e', nargs=2, help='Extra arguments, required by certain services')
def main(service, extra):
    """Console script for statuscheck."""
    try:
        service_api = get_statuscheck_api(service, extra_args=extra)
    except ModuleNotFoundError:
        click.echo(f'"{service}" is not implemented, leave a note at {__url__}')
        return 1
    except StatusCheckMissingArgumentsError as e:
        click.echo(str(e))
        return 1
    try:
        status = service_api.get_status()
    except StatusCheckParsingError as e:
        click.echo(str(e))
        return 1

    status_type = service_api.get_type()
    status_color = STATUSES_COLORS_MAPPING.get(status_type, '')
    incident = service_api.get_active_incident()

    if incident:
        click.echo(f'{status_color}{status_type or status}: {incident}')
        click.echo(f'More: {service_api.status_url}')
    else:
        click.echo(f'{status_color}{status_type or status}')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
