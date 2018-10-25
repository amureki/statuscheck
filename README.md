# statuscheck: Tool to check PAAS/SAAS status pages

[![Build Status](https://travis-ci.org/amureki/statuscheck.svg?branch=master)](https://travis-ci.org/amureki/statuscheck)
[![image](https://img.shields.io/pypi/v/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/l/statuscheck.svg)](https://pypi.org/project/statuscheck/)
[![image](https://img.shields.io/pypi/pyversions/statuscheck.svg)](https://pypi.org/project/statuscheck/)

## Usage

Install the latest release:

    $ pipenv install statuscheck

Then just use it in your shell:

```bash
$ statuscheck github
No issues
```

There is also an API available:

```python
from statuscheck.check import get_statuscheck_api

api = get_statuscheck_api('github')
status = api.get_status()
status_type = api.get_type()
```

Currently, all services that we support are defined [here](statuscheck/services/__init__.py).
