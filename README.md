# statuscheck: Tool to check PAAS/SAAS status pages

[![Build Status](https://travis-ci.org/amureki/statuscheck.svg?branch=master)](https://travis-ci.org/amureki/statuscheck)
[![image](https://img.shields.io/pypi/v/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/l/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/pyversions/statuscheck.svg)](https://pypi.org/project/statuscheck/)

## Usage

Install the latest release via `pip` or `pipenv`:

    $ pipenv install statuscheck

Then just use it in your shell:

```bash
$ statuscheck github
No issues

$ statuscheck slack
Incident: We're having issues with some features including the Events API, notifications, unfurls, and threads
More: https://status.slack.com/
```

There is also an API available:

```python
>>> from statuscheck.check import get_statuscheck_api

>>> api = get_statuscheck_api('slack')
>>> api.get_status()
"We're having issues with some features including the Events API, notifications, unfurls, and threads"
>>> api.get_type()
'Incident'
```

Currently, all services that we support are defined [here](statuscheck/services/__init__.py).
