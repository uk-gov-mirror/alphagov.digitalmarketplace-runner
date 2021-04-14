SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)
.DEFAULT_GOAL := run

export PATH := $(VIRTUALENV_ROOT)/bin:$(PATH)

PWD_PRETTY := $(subst $(HOME),$$HOME,$(shell pwd))

export COMPOSE_FILE := config/docker-compose.yml:config/docker-compose.$(shell uname).yml
export COMPOSE_PROJECT_NAME := dmrunner

MAIN_PY := python main.py

.PHONY: brew
brew:
	brew bundle
	pyenv install --skip-existing && pyenv version
	. Brewfile.env ; nvm install
	@tput bold
	@echo '😸 Prerequisites have been installed! 😸'
	@echo '😺 The following steps are recommended for a seamless experience 😺'
	@echo -ne '\x31\xEF\xB8\x8F\xE2\x83\xA3  ' # 1
	@echo -n 'Add the following lines to your shell profile (usually ~/.bash_profile):'
	@echo -e ' \x31\xEF\xB8\x8F\xE2\x83\xA3'
	@tput sgr0
	@echo
	@echo '[ -s "$(PWD_PRETTY)/Brewfile.env" ] && \'
	@echo '	. $(PWD_PRETTY)/Brewfile.env'
	@echo
	@tput bold
	@echo -ne '\x32\xEF\xB8\x8F\xE2\x83\xA3  ' # 2
	@echo -n 'Source the file now so you can continue with the next step:'
	@echo -e ' \x32\xEF\xB8\x8F\xE2\x83\xA3'
	@tput sgr0
	@echo
	@echo '$$ source Brewfile.env'
	@echo
	@tput bold
	@echo -ne '\x33\xEF\xB8\x8F\xE2\x83\xA3  ' # 3
	@echo -n 'Increase the memory limit of Docker for Mac to 4 GiB'
	@echo -e ' \x33\xEF\xB8\x8F\xE2\x83\xA3'
	@tput sgr0
	@echo
	@tput bold
	@echo -ne '\x34\xEF\xB8\x8F\xE2\x83\xA3  ' # 4
	@echo -n 'You can now try continuing the setup!'
	@echo -e ' \x34\xEF\xB8\x8F\xE2\x83\xA3'
	@tput sgr0
	@echo
	@echo '$$ make setup'
	@echo
	@tput bold
	@echo '😹 Good luck! 😹'
	@tput sgr0

.PHONY: virtualenv
virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && python3 -m venv venv || true

.PHONY: install
install: virtualenv
	pip install --upgrade pip wheel
	pip install -r requirements.txt

.PHOHY: config
config: install
	$(MAIN_PY) config

.PHOHY: setup
setup: install
	$(MAIN_PY) ${ARGS} setup

.PHOHY: data
data: install
	$(MAIN_PY) ${ARGS} data

.PHONY: run
run: virtualenv
	$(MAIN_PY) ${ARGS} run

.PHONY: rebuild
rebuild: virtualenv
	$(MAIN_PY) --rebuild ${ARGS} run

.PHONY: nix
nix: virtualenv
	$(MAIN_PY) --nix ${ARGS} run

.PHONY: nix-rebuild
nix-rebuild: virtualenv
	$(MAIN_PY) --nix --rebuild ${ARGS} run

.PHONY: black
black: install
	black config/ dmrunner/ main.py setup.py

.PHONY: test-black
test-black: install
	black --check config/ dmrunner/ main.py setup.py

.PHONY: test-mypy
test-mypy: install
	mypy dmrunner/ main.py setup.py

.PHONY: test-pyflakes
test-pyflakes: install
	pyflakes config/ dmrunner/ main.py setup.py

.PHONY: test
test: test-black test-mypy test-pyflakes

.PHONY: update-code
update-code:
	invoke update-code


# Export docker-compose using dmrunner files and project name.
# Saves having to remember to type them out yourself.
# Use with `eval "$(make docker-compose-env)"`
.PHONY: docker-compose-env
docker-compose-env:
	export COMPOSE_FILE='$(COMPOSE_FILE)'
	export COMPOSE_PROJECT_NAME='$(COMPOSE_PROJECT_NAME)'
