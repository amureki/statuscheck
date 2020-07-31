from typing import List

import attr

STATUS_OK = "ok"
STATUS_ACTIVE = "active"
STATUS_RESOLVED = "resolved"
STATUS_SCHEDULED = "scheduled"
STATUS_COMPLETED = "completed"
STATUS_CANCELED = "canceled"

STATUS_TYPE_MAPPING = {
    STATUS_OK: "No issues",
    STATUS_ACTIVE: "Active incident",
    STATUS_RESOLVED: "Resolved incident",
    STATUS_SCHEDULED: "Scheduled maintenance",
    STATUS_COMPLETED: "Completed maintenance",
    STATUS_CANCELED: "Canceled maintenance",
}


@attr.s(auto_attribs=True)
class Component:
    name: str


@attr.s(auto_attribs=True)
class Incident:
    id: str
    title: str
    status: str = attr.ib(validator=attr.validators.in_(STATUS_TYPE_MAPPING.keys()))
    type: str = attr.ib(validator=attr.validators.in_(["incident", "notice", "outage"]))
    components: List[Component] = attr.ib(
        default=[], validator=attr.validators.instance_of(list),
    )


@attr.s(auto_attribs=True)
class Status:
    code: str = attr.ib(validator=attr.validators.in_(STATUS_TYPE_MAPPING.keys()))
    description: str


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
