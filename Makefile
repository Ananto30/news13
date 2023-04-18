SHELL := /bin/bash

setup:
	python3 -m venv venv
	source venv/bin/activate && ( \
		pip install -r script/requirements.txt; \
		pip install black isort flake8 pylint pytype mypy; \
		)

format:
	isort . --profile black -l 99
	black .

install-lint:
	python -m pip install --upgrade pip
	pip install -r requirements.txt  # needed for pytype
	pip install black isort flake8 pylint pytype mypy

lint:
	flake8 ./scripts
	pylint ./scripts
	# pytype ./scripts
	mypy ./scripts
