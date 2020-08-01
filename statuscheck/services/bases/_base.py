import click


class BaseServiceAPI:
    name: str = None
    summary = None
    service_url: str = None
    status_url: str = None

    @property
    def _module_name(self):
        module_relpath = self.__class__.__module__
        return module_relpath.rsplit(".", 1)[1]

    def __init__(self):
        self.summary = self.get_summary()

    def get_summary(self):
        raise NotImplementedError

    def _print_summary(self, verbose=False):
        click.echo(f"Current {self.name} status: {self.summary.status.name}")

        incidents = self.summary.incidents
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

        if incidents or not self.summary.status.is_ok:
            click.echo()
            click.echo(f"More: {self.status_url}")
