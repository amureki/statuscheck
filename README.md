
# statuscheck: Tool to check PAAS/SAAS status pages

![Tests](https://github.com/amureki/statuscheck/workflows/Tests/badge.svg)
[![image](https://img.shields.io/pypi/v/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/l/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/pyversions/statuscheck.svg)](https://pypi.org/project/statuscheck/)

## Usage

Install the latest release via `pip` or `pipenv`:

    $ pipenv install statuscheck

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
    Status(code='active', description='Active incident')
    >>> summary.incidents
    [Incident(id=878, name='We are investigating an issue with notification settings', status='active', components=[Component(name='Notifications', status='', id='')]), Incident(id=879, name="We're looking into an issue with certain API calls", status='active', components=[Component(name='Apps/Integrations/APIs', status='', id='')])]


Currently, all services that we support are defined [here](statuscheck/services/__init__.py).
