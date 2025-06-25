# customer_segmentation

This repository contains jupyter notebooks analyzing customer data.

src/customer_segmentation/ contains source code.

---

## Structure
```bash
customer_segmentation/
├── Makefile
├── README.md
├── data
├── docs
│   └── customer_segmentation.md
├── notebooks
│   ├── EDA.ipynb
│   ├── RFM.ipynb
│   └── Segmentation.ipynb
├── pyproject.toml
├── requirements-dev.txt
├── src
│   ├── customer_segmentation
│   │   ├── __init__.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── functions.py
│   │       └── sql
│   │           └── customer_data_model.sql
└── tests
```

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone git@github.com:bfreiheit/customer_segmentation.git
cd customer_segmentation
```
### 2. (Optional) Set up a virtual environment
It is recommended creating a single virtual environment at the top level:
```bash
make venv
source .venv/bin/activate
```
### 3. Install project dependencies
```bash
make install
```
### 4. (Optional) Install development dependencies
If you need linters, testing tools, etc.:
```bash
make install-dev
```
### 5. Other useful Makefile commands

Run `make help` to see all available commands.

| Command         | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `make update`   | Reinstalls the project as editable (`pip install -e .`).     |
| `make notebook` | Starts a Jupyter Notebook in `./notebooks`.                  |
| `make clean`    | Deletes all `__pycache__` directories.                       |
| `make freeze`   | Lists all installed packages.                                |
| `make lint`     | Runs `flake8` on `src/`, `notebooks/`, and `tests/`.         |
| `make format`   | Auto-formats all source files with `black`.                  |
| `make isort`    | Sorts all imports with `isort`.                              |
| `make check`    | Runs `lint`, `format`, and `isort`.                          |

### 6. Run Tests
Run tests with:
```bash
pytest tests
