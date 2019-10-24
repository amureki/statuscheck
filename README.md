# statuscheck: Tool to check PAAS/SAAS status pages

[![Build Status](https://travis-ci.org/amureki/statuscheck.svg?branch=master)](https://travis-ci.org/amureki/statuscheck)
[![image](https://img.shields.io/pypi/v/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/l/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/pyversions/statuscheck.svg)](https://pypi.org/project/statuscheck/)

## Usage

Install the latest release via `pip` or `pipenv`:

    $ pipenv install statuscheck

Then just use it in your shell:

    $ statuscheck github
    Current status of GitHub: No issues

    $ statuscheck digitalocean
    Current status of DigitalOcean: Minor incident
    Registered incidents:
    - DNS issues with Managed Databases [Identified]
    - Issues with accessing S3/RDS resources inside Droplets across all regions [Monitoring]
    Affected components:
    - Services: Degraded performance
    - Managed Databases: Degraded performance
    - Spaces: Degraded performance

    More: https://status.digitalocean.com/

There is also an API available:


    >>> from statuscheck.check import get_statuscheck_api

    >>> api = get_statuscheck_api('digitalocean')
    >>> summary = api.get_summary()
    >>> summary.status
    'Minor incident'
    >>> summary.incidents
    [{'name': 'DNS issues with Managed Databases', 'status': 'Identified', 'impact': 'minor'}, {'name': 'Issues with accessing S3/RDS resources inside Droplets across all regions', 'status': 'Monitoring', 'impact': 'minor'}]


Currently, all services that we support are defined [here](statuscheck/services/__init__.py).
