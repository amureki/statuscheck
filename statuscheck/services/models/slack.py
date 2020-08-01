from typing import List

import attr

from statuscheck.services.models.generic import (
    TYPE_GOOD,
    TYPE_INCIDENT,
    TYPE_MAINTENANCE,
)

STATUS_OK = "ok"
STATUS_ACTIVE = "active"
STATUS_RESOLVED = "resolved"
STATUS_SCHEDULED = "scheduled"
STATUS_COMPLETED = "completed"
STATUS_CANCELED = "canceled"

STATUS_TYPE_MAPPING = {
    STATUS_OK: TYPE_GOOD,
    STATUS_ACTIVE: TYPE_INCIDENT,
    STATUS_RESOLVED: TYPE_INCIDENT,
    STATUS_SCHEDULED: TYPE_MAINTENANCE,
    STATUS_COMPLETED: TYPE_MAINTENANCE,
    STATUS_CANCELED: TYPE_MAINTENANCE,
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

    @property
    def is_ok(self):
        return self.code == STATUS_OK


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
