.ONESHELL:
UV ?= uv
UV_CACHE_DIR ?= .uv-cache
UV_CMD = UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV)

.PHONY: help
help:             	## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: venv
venv:			## Create a virtual environment
	@echo "Creating virtualenv with uv ..."
	@rm -rf .venv
	@$(UV_CMD) venv .venv
	@echo
	@echo "Run '$(UV_CMD) sync --group dev --group test' to install dependencies"

.PHONY: install
install:		## Install dependencies
	$(UV_CMD) sync --group dev --group test

STRESS_URL = http://127.0.0.1:8000
.PHONY: stress-test
stress-test:
	# change stress url to your deployed app
	mkdir -p reports
	if [ -x .venv/bin/locust ]; then \
		.venv/bin/locust -f tests/stress/api_stress.py --print-stats --html reports/stress-test.html --run-time 60s --headless --users 100 --spawn-rate 1 -H $(STRESS_URL); \
	else \
		$(UV_CMD) run --group test locust -f tests/stress/api_stress.py --print-stats --html reports/stress-test.html --run-time 60s --headless --users 100 --spawn-rate 1 -H $(STRESS_URL); \
	fi

.PHONY: model-test
model-test:			## Run tests and coverage
	mkdir -p reports
	if [ -x .venv/bin/pytest ]; then \
		cd tests && PYTHONPATH=.. ../.venv/bin/pytest --cov-config=.coveragerc --cov-report term --cov-report html:../reports/html --cov-report xml:../reports/coverage.xml --junitxml=../reports/junit.xml --cov=challenge model; \
	else \
		cd tests && PYTHONPATH=.. $(UV_CMD) run --group test pytest --cov-config=.coveragerc --cov-report term --cov-report html:../reports/html --cov-report xml:../reports/coverage.xml --junitxml=../reports/junit.xml --cov=challenge model; \
	fi

.PHONY: api-test
api-test:			## Run tests and coverage
	mkdir -p reports
	if [ -x .venv/bin/pytest ]; then \
		.venv/bin/pytest --cov-config=.coveragerc --cov-report term --cov-report html:reports/html --cov-report xml:reports/coverage.xml --junitxml=reports/junit.xml --cov=challenge tests/api; \
	else \
		$(UV_CMD) run --group test pytest --cov-config=.coveragerc --cov-report term --cov-report html:reports/html --cov-report xml:reports/coverage.xml --junitxml=reports/junit.xml --cov=challenge tests/api; \
	fi

.PHONY: build
build:			## Build locally the python artifact
	$(UV_CMD) build

.PHONY: precommit-scoped
precommit-scoped:	## Run pre-commit for process files tracked in release
	FILES="$$(find tools openspec -type f)"; \
	pre-commit run --files AGENTS.md .pre-commit-config.yaml pyproject.toml $$FILES

.PHONY: pc
pc: precommit-scoped	## Short alias for precommit-scoped
