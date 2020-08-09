
# statuscheck: Tool to check PAAS/SAAS status pages

![Tests](https://github.com/amureki/statuscheck/workflows/Tests/badge.svg)
[![image](https://img.shields.io/pypi/v/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/l/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/pyversions/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![Coverage Status](https://coveralls.io/repos/github/amureki/statuscheck/badge.svg)](https://coveralls.io/github/amureki/statuscheck)

## Usage

Install the latest release:

    $ pip install statuscheck

Then just use it in your shell:

    $ statuscheck github
    Current GitHub status: All Systems Operational

    $ statuscheck slack
    Current Slack status: Active incident
    Registered events:
    - [active] We are investigating an issue with notification settings
    - [active] We're looking into an issue with certain API calls

    More: https://status.slack.com/

There is also an API available:


    >>> from statuscheck.utils import get_statuscheck_api

    >>> api = get_statuscheck_api('slack')
    >>> summary = api.get_summary()
    >>> summary.status
    Status(code='active', name='Minor incident', description='Minor incident', is_ok=False)
    >>> summary.incidents
    [Incident(id=879, name="We're looking into an issue with certain API calls", status='active', components=[Component(name='Apps/Integrations/APIs', status='', id='')])]
    >>> summary.as_dict()
    {'status': {'code': 'active', 'name': 'Minor incident', 'description': 'Minor incident', 'is_ok': False}, 'components': [{'name': 'Apps/Integrations/APIs', 'status': '', 'id': ''}], 'incidents': [{'id': 879, 'name': "We're looking into an issue with certain API calls", 'status': 'active', 'components': [{'name': 'Apps/Integrations/APIs', 'status': '', 'id': ''}]}]}


Currently, all services that we support are defined [here](statuscheck/services/__init__.py).
