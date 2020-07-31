from typing import List

import attr


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
