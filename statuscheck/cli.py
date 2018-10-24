import sys
import click

from .__about__ import __url__
from statuscheck.check import get_statuscheck_api
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
def main(service):
    """Console script for statuscheck."""
    try:
        service_api = get_statuscheck_api(service)
    except ModuleNotFoundError:
        click.echo(f'"{service}" is not implemented, leave a note at {__url__}')
        return 0
    status = service_api.get_status()
    status_type = service_api.get_status_type()
    status_color = STATUSES_COLORS_MAPPING.get(status_type, '')
    if status_type:
        click.echo(f'{status_color}{status_type}')
    else:
        click.echo(f'{status_color}{status}')

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
