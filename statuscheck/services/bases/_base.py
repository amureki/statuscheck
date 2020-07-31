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

    def _print_summary(self):
        click.echo(f"Current {self.name} status: {self.summary.status.description}")

        incidents = self.summary.incidents
        if incidents:
            click.echo(f"Registered events:")
            for incident in incidents:
                if incident.status:
                    click.echo(f"- [{incident.status}] {incident.name}")
                else:
                    click.echo(f"- {incident.name}")
                if hasattr(incident, "scheduled_for") and incident.scheduled_for:
                    click.echo(f"  {incident.scheduled_for}")
                # TODO: verbosity 2?
                if incident.components:
                    click.echo(f"  Affected components:")
                    for component in incident.components:
                        if component.status:
                            click.echo(f"    - {component.name} [{component.status}]")
                        else:
                            click.echo(f"    - {component.name}")

        # TODO: if status not OK?
        if incidents:
            click.echo()
            click.echo(f"More: {self.status_url}")
