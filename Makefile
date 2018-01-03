SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)
.DEFAULT_GOAL := run

.PHONY: virtualenv
virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && virtualenv -p python3 venv || true

.PHONY: install
install: virtualenv
	${VIRTUALENV_ROOT}/bin/pip install -r requirements.txt 

.PHOHY: config
config: install
	${VIRTUALENV_ROOT}/bin/python main.py config

.PHOHY: setup
setup: install
	${VIRTUALENV_ROOT}/bin/python main.py setup

.PHONY: run
run: virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py ${ARGS} run

.PHONY: all
all: virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py --all ${ARGS} run

.PHONY: nix
nix: virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py --nix ${ARGS} run

.PHONY: nix-all
nix-all:  virtualenv
	${VIRTUALENV_ROOT}/bin/python main.py --nix --all ${ARGS} run
