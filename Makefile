VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

venv:
	python -m venv $(VENV_DIR)

install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .

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
	$(VENV_DIR)/bin/isort src notebooks tests

check:
	make lint
	make format
	make isort

help:
	@echo "available targets:"
	@echo "  make venv       → erstellt die venv"
	@echo "  make install    → installs project from pyproject.toml"
	@echo "  make update     → update project/dependencies"
	@echo "  make notebook   → starts Jupyter Notebook in ./notebooks"
	@echo "  make clean      → deletes __pycache__ directories"
	@echo "  make freeze     → lists installed packages"
	@echo "  make lint       → runs flake8 on src, notebooks, tests"
	@echo "  make format     → auto-formats with black"
	@echo "  make isort      → sorts imports with isort"
	@echo "  make check      → runs lint, foramt and isort"