VENV_DIR := .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

venv:
	python3 -m venv $(VENV_DIR)

install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .

install-dev: install
	$(PIP) install -r requirements-dev.txt

update:
	$(PIP) install -e .

notebook:
	$(PYTHON) -m notebook notebooks/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

freeze:
	$(PIP) freeze

lint:
	$(VENV_DIR)/bin/flake8 src notebooks tests

format:
	$(VENV_DIR)/bin/black src notebooks tests

isort:
	$(VENV_DIR)/bin/isort src tests
	$(VENV_DIR)/bin/nbqa isort notebooks

check:
	make lint
	make format
	make isort

help:
	@echo "available targets:"
	@echo "  make venv       → creates venv"
	@echo "  make install    → installs project from pyproject.toml"
	@echo "  make install-dev → installs projects and dev-dependencies"
	@echo "  make update     → update project/dependencies"
	@echo "  make notebook   → starts Jupyter Notebook in ./notebooks"
	@echo "  make clean      → deletes __pycache__ directories"
	@echo "  make freeze     → lists installed packages"
	@echo "  make lint       → runs flake8 on src, notebooks, tests"
	@echo "  make format     → auto-formats with black"
	@echo "  make isort      → sorts imports with isort"
	@echo "  make check      → runs lint, foramt and isort"