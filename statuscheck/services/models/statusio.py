from datetime import datetime
from typing import List

import attr

from statuscheck.services.models.generic import (
    TYPE_GOOD,
    TYPE_INCIDENT,
    TYPE_OUTAGE,
    TYPE_SECURITY,
)

STATUS_OK = 100
STATUS_DEGRADED_PERFORMANCE = 300
STATUS_PARTIAL_SERVICE_DISRUPTION = 400
STATUS_MAJOR = 500
STATUS_SECURITY = 600

STATUS_TYPE_MAPPING = {
    STATUS_OK: TYPE_GOOD,
    STATUS_DEGRADED_PERFORMANCE: TYPE_INCIDENT,
    STATUS_PARTIAL_SERVICE_DISRUPTION: TYPE_INCIDENT,
    STATUS_MAJOR: TYPE_OUTAGE,
    STATUS_SECURITY: TYPE_SECURITY,
}


@attr.s(auto_attribs=True)
class Component:
    id: str
    name: str
    updated: datetime = attr.ib(default=None)
    status: str = attr.ib(default=None)
    status_code: int = attr.ib(default=None)


@attr.s(auto_attribs=True)
class Incident:
    _id: str
    name: str
    datetime_open: datetime
    components: List[Component] = attr.ib(
        default=[],
        validator=attr.validators.optional(attr.validators.instance_of(list)),
    )


@attr.s(auto_attribs=True)
class Status:
    description: str
    status_code: int
    updated: datetime

    @property
    def is_ok(self):
        return self.status_code == 100


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
