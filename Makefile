SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)
.DEFAULT_GOAL := run

PWD_PRETTY := $(subst $(HOME),$$HOME,$(shell pwd))

export COMPOSE_PROJECT_NAME := dmrunner

.PHONY: brew
brew:
	brew bundle
	pyenv install --skip-existing && pyenv version
	. Brewfile.env ; nvm install && npm install -g yarn
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
