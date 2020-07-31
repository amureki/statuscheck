import sys
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

import click

from statuscheck.__about__ import __url__
from statuscheck.services import SERVICES
from statuscheck.utils import get_statuscheck_api


@click.command()
@click.argument("service")
@click.option("-v", "--verbose", is_flag=True, help="More verbose mode")
def main(service, verbose):
    if service == "all":
        _check_all(verbose)
        return 0

    try:
        service_api = get_statuscheck_api(service)
    except ModuleNotFoundError:
        click.echo(f'"{service}" is not implemented, leave a note at {__url__}')
        return 1

    service_api._print_summary(verbose=verbose)
    return 0


def _parse_api_summary(service):
    service_api = get_statuscheck_api(service)
    return service_api


def _check_all(verbose):
    click.echo(f"Parsing {len(SERVICES)} services...")
    with PoolExecutor(max_workers=8) as executor:
        services = []
        for service in executor.map(_parse_api_summary, SERVICES):
            services.append(service)
    for service_api in services:
        service_api._print_summary(verbose)
        click.echo("=" * 40)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
