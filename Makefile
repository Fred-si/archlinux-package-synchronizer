.DEFAULT_GOAL = setup
.PHONY: help setup teardown

help: ## Print this help
	@grep -hE '(^[a-z][a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST)\
		| awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-12s$(NO_COLOR) %s\n", $$1, $$2}'\
		| sed -e 's/\[32m##/[33m/'

setup: install git-hooks ## Setup development environment

teardown: ## Delete generated files and venv
	rm -rf venv dist build src/*.egg-info .ruff_cache .pytest_cache .mypy_cache
	find . -name '__pycache__' | xargs rm -rf

install: venv/lib/python3.13/site-packages/archlinux_package_synchronizer*
venv/lib/python3.13/site-packages/archlinux_package_synchronizer*: venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements-dev.txt
	./venv/bin/pip install -e '.'
	./venv/bin/mypy --install-types --non-interactive . || true

git-hooks: .git/hooks/pre-commit
.git/hooks/pre-commit: venv/bin/pre-commit
	./venv/bin/pre-commit install --install-hooks

pip-upgrade: pip-compile pip-sync ## Upgrade project dependencies

pip-compile: venv/bin/pip-compile ## Compile pyproject.toml dependencies to requirements files
	./venv/bin/pip-compile --upgrade --strip-extras --output-file requirements.txt
	./venv/bin/pip-compile --upgrade --strip-extras --extra dev --output-file requirements-dev.txt

pip-sync: venv/bin/pip-sync ## Synchronize installed packages to requirements-dev.txt
	./venv/bin/pip-sync requirements-dev.txt

venv/bin/pre-commit: install
venv/bin/pip-compile: install
venv/bin/pip-sync: install

venv:
	python -m venv venv
