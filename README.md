# Customer Segmentation

This repository contains jupyter notebooks analyzing customer data:
- [EDA-Notebook](../notebooks/EDA.ipynb)
- [Segmentation-Notebook](../notebooks/Segmentation.ipynb)
- [RFM-Notebook](../notebooks/RFM.ipynb)

In the docs/ folder the data model and analysis is explained:  
- [Data Model](../docs/data_model.md)  
- [Segmentation Documentation](../docs/customer_segmentation.md)  
- [Video Recording](https://www.loom.com/share/7d18488920a9420889f59ce04ef76719?sid=3b420213-1958-46ea-a336-03a443f8a883)  
- [Segmentation Presentation](../docs/Customer_Segmentation_Presentation.pdf)

src/customer_segmentation/ contains source code.

---

## Structure
```bash
customer_segmentation/
├── Makefile
├── README.md
├── data
│   ├── RFM_analysis_results.csv
│   └── segmentation_results.csv
├── docs
│   ├── Customer Segmentation_Presentation.pdf
│   ├── customer_segmentation.md
│   └── data_model.md
├── images
│   ├── gmm_cluster_table.png
│   ├── kmeans_cluster_table.png
│   ├── rfm_cluster_groups_table.png
│   ├── rfm_groups_table.png
│   └── segmentation_table.png
├── notebooks
│   ├── EDA.ipynb
│   ├── Preprocessing.ipynb
│   ├── RFM.ipynb
│   └── Segmentation.ipynb
├── pyproject.toml
├── requirements-dev.txt
├── sql
│   ├── create_customer_cohort.sql
│   ├── create_customer_features.sql
│   ├── customer_cohort_model_local.sql
│   ├── customer_data_model.sql
│   ├── customer_features_local.sql
│   └── data_exploration.sql
├── src
│   ├── customer_segmentation
│   │   ├── __init__.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── db_utils.py
│   │       ├── file_io.py
│   │       ├── plot_utils.py
│   │       └── preprocessing.py
└── tests
    └── test_preprocessing.py
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
```
### 7. Create .env file
Structure of the file:  
DB_HOST=localhost        # e.g. 'db.example.com'  
DB_PORT=5432             # e.g. 3306 for MySQL  
DB_USER=admin  
DB_PASSWORD=yourpassword  