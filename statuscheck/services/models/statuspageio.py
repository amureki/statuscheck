from typing import List

import attr

STATUS_NONE = "none"
STATUS_MINOR = "minor"
STATUS_MAJOR = "major"
STATUS_CRITICAL = "critical"
STATUS_MAINTENANCE = "maintenance"

STATUS_TYPE_MAPPING = {
    STATUS_NONE: "No issues",
    STATUS_MINOR: "Minor incident",
    STATUS_MAJOR: "Major outage",
    STATUS_CRITICAL: "Critical incident",
    STATUS_MAINTENANCE: "Maintenance",
}


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
    impact: str = attr.ib(validator=attr.validators.in_(STATUS_TYPE_MAPPING.keys()))
    scheduled_for: str
    scheduled_until: str
    components: List[Component] = attr.ib(
        default=[],
        validator=attr.validators.optional(attr.validators.instance_of(list)),
    )


@attr.s(auto_attribs=True)
class Status:
    description: str
    indicator: str = attr.ib(validator=attr.validators.in_(STATUS_TYPE_MAPPING.keys()))

    @property
    def is_ok(self):
        return self.indicator == STATUS_NONE


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