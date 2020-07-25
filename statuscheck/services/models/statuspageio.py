from typing import List

import attr


@attr.s(auto_attribs=True)
class Component:
    id: str
    description: str
    status: str = attr.ib(
        validator=attr.validators.in_(
            [
                "operational",
                "under_maintenance",
                "degraded_performance",
                "partial_outage",
                "major_outage",
                "",
            ]
        )
    )
    name: str
    only_show_if_degraded: bool


@attr.s(auto_attribs=True)
class Incident:
    id: str
    name: str
    status: str = attr.ib(
        validator=attr.validators.in_(
            [
                "investigating",
                "identified",
                "monitoring",
                "resolved",
                "scheduled",
                "in_progress",
                "verifying",
                "completed",
            ]
        )
    )
    impact: str = attr.ib(
        validator=attr.validators.in_(
            ["none", "minor", "major", "critical", "maintenance"]
        )
    )
    scheduled_for: str
    scheduled_until: str
    components: List[Component] = attr.ib(
        default=[],
        validator=attr.validators.optional(attr.validators.instance_of(list)),
    )


@attr.s(auto_attribs=True)
class Status:
    description: str
    indicator: str = attr.ib(
        validator=attr.validators.in_(
            ["none", "minor", "major", "critical", "maintenance"]
        )
    )


@attr.s(auto_attribs=True)
class Summary:
    status: Status
    components: List[Component] = attr.ib(
        default=[],
        validator=attr.validators.optional(attr.validators.instance_of(list)),
    )
    incidents: List[Incident] = attr.ib(
        default=[],
        validator=attr.validators.optional(attr.validators.instance_of(list)),
    )
