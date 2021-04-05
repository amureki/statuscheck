from typing import Optional

import click
from httpx import TransportError

from statuscheck.services.models.generic import Summary


class BaseServiceAPI:
    name: str = ""
    summary: Optional[Summary] = None
    service_url: str = ""
    status_url: str = ""

    @property
    def _module_name(self):
        module_relpath = self.__class__.__module__
        return module_relpath.rsplit(".", 1)[1]

    def get_summary(self):
        raise NotImplementedError

    def _print_summary(self, verbose=False):
        try:
            summary = self.get_summary()
        except TransportError as e:
            click.echo(f"Cannot fetch {self.name} status due to {type(e)}:")
            click.echo(str(e))
            click.echo("\nPlease, try again.")
            return
        click.echo(f"Current {self.name} status: {summary.status.name}")

        incidents = summary.incidents
        if incidents:
            click.echo("Registered events:")
            for incident in incidents:
                if incident.status:
                    click.echo(f"- [{incident.status}] {incident.name}")
                else:
                    click.echo(f"- {incident.name}")
                if hasattr(incident, "scheduled_for") and incident.scheduled_for:
                    click.echo(f"  {incident.scheduled_for}")

                if verbose and incident.components:
                    click.echo("  Affected components:")
                    for component in incident.components:
                        if component.status:
                            click.echo(f"    - {component.name} [{component.status}]")
                        else:
                            click.echo(f"    - {component.name}")

        if incidents or not summary.status.is_ok:
            click.echo(f"\nMore: {self.status_url}")
