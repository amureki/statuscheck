from typing import List

import attr

from statuscheck.services.models.generic import (
    TYPE_GOOD,
    TYPE_INCIDENT,
    TYPE_MAINTENANCE,
    TYPE_OUTAGE,
)

STATUS_GREEN = "green"
STATUS_YELLOW = "yellow"
STATUS_RED = "red"
STATUS_BLUE = "blue"

STATUS_TYPE_MAPPING = {
    STATUS_GREEN: TYPE_GOOD,
    STATUS_YELLOW: TYPE_INCIDENT,
    STATUS_RED: TYPE_OUTAGE,
    STATUS_BLUE: TYPE_MAINTENANCE,
}


@attr.s(auto_attribs=True)
class Component:
    name: str
    status: str


@attr.s(auto_attribs=True)
class Incident:
    id: str
    title: str
    state: str
    components: List[Component] = attr.ib(
        default=[], validator=attr.validators.instance_of(list),
    )


@attr.s(auto_attribs=True)
class Status:
    code: str = attr.ib(validator=attr.validators.in_(STATUS_TYPE_MAPPING.keys()))
    description: str

    @property
    def is_ok(self):
        return self.code == STATUS_GREEN


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
