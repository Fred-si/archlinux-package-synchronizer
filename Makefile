.DEFAULT_GOAL = setup
.PHONY: help setup git-hooks install teardown

help: ## Print this help
	@grep -hE '(^[a-z][a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST)\
		| awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-12s$(NO_COLOR) %s\n", $$1, $$2}'\
		| sed -e 's/\[32m##/[33m/'

setup: install git-hooks

install: venv/lib/python3.13/site-packages/archlinux_package_synchronizer*
venv/lib/python3.13/site-packages/archlinux_package_synchronizer*: venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements-dev.txt
	./venv/bin/pip install -e '.'
	./venv/bin/mypy --install-types --non-interactive . || true

git-hooks: venv/bin/pre-commit .git/hooks/pre-commit
venv/bin/pre-commit: install
.git/hooks/pre-commit: venv/bin/pre-commit
	./venv/bin/pre-commit install --install-hooks

pip-compile: venv/bin/pip-compile
	./venv/bin/pip-compile --upgrade --strip-extras --output-file requirements.txt
	./venv/bin/pip-compile --upgrade --strip-extras --extra dev --output-file requirements-dev.txt
	./venv/bin/pip-sync requirements-dev.txt

venv/bin/pip-compile: install
teardown: ## Delete generated files and venv
	rm -rf venv dist build src/*.egg-info .ruff_cache .pytest_cache .mypy_cache
	find . -name '__pycache__' | xargs rm -rf

venv:
	python -m venv venv
