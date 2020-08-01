from typing import List

import attr

TYPE_GOOD = "No issues"
TYPE_MAINTENANCE = "Maintenance"
TYPE_INCIDENT = "Minor incident"
TYPE_OUTAGE = "Major outage"
TYPE_CRITICAL = "Critical incident"
TYPE_SECURITY = "Security incident"
TYPE_UNKNOWN = ""

STATUS_TYPES = (
    TYPE_GOOD,
    TYPE_MAINTENANCE,
    TYPE_INCIDENT,
    TYPE_OUTAGE,
    TYPE_CRITICAL,
    TYPE_SECURITY,
    TYPE_UNKNOWN,
)


@attr.s(auto_attribs=True)
class Component:
    name: str
    status: str = attr.ib(default="")
    id: str = attr.ib(default="")


@attr.s(auto_attribs=True)
class Incident:
    id: str
    name: str
    status: str = attr.ib(default="")
    components: List[Component] = attr.ib(
        default=[], validator=attr.validators.instance_of(list),
    )


@attr.s(auto_attribs=True)
class Status:
    code: str
    name: str = attr.ib(validator=attr.validators.in_(STATUS_TYPES))
    description: str
    is_ok: bool


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

    def as_dict(self) -> dict:
        return attr.asdict(self)
