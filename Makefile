 lint:
	flake8
	pydocstyle
	isort --diff --check-only --recursive
	bandit -r statuscheck
	black --check .
