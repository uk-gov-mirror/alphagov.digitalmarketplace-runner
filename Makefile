SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)
.DEFAULT_GOAL := run

export COMPOSE_PROJECT_NAME := dmrunner

.PHONY: virtualenv
virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && python3 -m venv venv || true

.PHONY: install
install: virtualenv
	${VIRTUALENV_ROOT}/bin/pip install -r requirements.txt 

.PHOHY: config
config: install
	${VIRTUALENV_ROOT}/bin/python main.py config

.PHOHY: setup
setup: install
	${VIRTUALENV_ROOT}/bin/python main.py ${ARGS} setup

.PHOHY: data
data: install
	${VIRTUALENV_ROOT}/bin/python main.py ${ARGS} data

.PHONY: run
run: virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py ${ARGS} run

.PHONY: rebuild
rebuild: virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py --rebuild ${ARGS} run

.PHONY: nix
nix: virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py --nix ${ARGS} run

.PHONY: nix-rebuild
nix-rebuild: virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py --nix --rebuild ${ARGS} run

.PHONY: black
black: install
	${VIRTUALENV_ROOT}/bin/black config/ dmrunner/ main.py setup.py

.PHONY: test-black
test-black: install
	${VIRTUALENV_ROOT}/bin/black --check config/ dmrunner/ main.py setup.py

.PHONY: test-mypy
test-mypy: install
	${VIRTUALENV_ROOT}/bin/mypy dmrunner/ main.py setup.py

.PHONY: test-pyflakes
test-pyflakes: install
	${VIRTUALENV_ROOT}/bin/pyflakes config/ dmrunner/ main.py setup.py

.PHONY: test
test: test-black test-mypy test-pyflakes
