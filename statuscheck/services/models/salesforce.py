from typing import List

import attr

STATUS_OK = "OK"
STATUS_CORE_OUTAGE = "MAJOR_INCIDENT_CORE"
STATUS_NONCORE_OUTAGE = "MAJOR_INCIDENT_NONCORE"
STATUS_CORE_INCIDENT = "MINOR_INCIDENT_CORE"
STATUS_NONCORE_INCIDENT = "MINOR_INCIDENT_NONCORE"
STATUS_CORE_MAINTENANCE = "MAINTENANCE_CORE"
STATUS_NONCORE_MAINTENANCE = "MAINTENANCE_NONCORE"

# sorted by severity
NOT_GOOD_STATUSES = [
    STATUS_CORE_OUTAGE,
    STATUS_NONCORE_OUTAGE,
    STATUS_CORE_INCIDENT,
    STATUS_NONCORE_INCIDENT,
    STATUS_CORE_MAINTENANCE,
    STATUS_NONCORE_MAINTENANCE,
]

STATUS_TYPE_MAPPING = {
    STATUS_OK: "No issues",
    STATUS_CORE_INCIDENT: "Minor incident",
    STATUS_NONCORE_INCIDENT: "Minor incident",
    STATUS_CORE_OUTAGE: "Major outage",
    STATUS_NONCORE_OUTAGE: "Major outage",
    STATUS_CORE_MAINTENANCE: "Minor incident",
    STATUS_NONCORE_MAINTENANCE: "Minor incident",
}


@attr.s(auto_attribs=True)
class Component:
    key: str
    location: str
    environment: str
    status: str = attr.ib(validator=attr.validators.in_(STATUS_TYPE_MAPPING.keys()))
    is_active: bool


@attr.s(auto_attribs=True)
class Incident:
    id: int
    affects_all: bool
    is_core: bool
    type: str
    instance_keys: list
    status: str = attr.ib(validator=attr.validators.in_(STATUS_TYPE_MAPPING.keys()))
    text: str = attr.ib(default="")
    components: List[Component] = attr.ib(
        default=[], validator=attr.validators.instance_of(list),
    )


@attr.s(auto_attribs=True)
class Status:
    code: str
    description: str = attr.ib(default="")

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
