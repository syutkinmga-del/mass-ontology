.PHONY: validate test tree status

PYTHON := .venv/bin/python

validate:
	$(PYTHON) scripts/run_shacl.py

test:
	$(PYTHON) -m pytest

tree:
	tree -I ".venv|__pycache__|.git"

status:
	git status
