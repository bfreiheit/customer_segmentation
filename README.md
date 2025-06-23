# customer_segmentation

This repository contains multiple analysis projects, each in its own subfolder.

Each project is self-contained, with its own source code and optional dependencies.

---

## Structure
```bash
analysis_collection/
├── Makefile
├── README.md
├── requirements.txt
├── setup.py
├── travel_tide
│   ├── __init__.py│   
│   ├── data
│   ├── notebooks
│   │   ├── EDA.ipynb
│   │   ├── RFM.ipynb
│   │   └── Segmentation.ipynb
│   └── utils
│       ├── __init__.py│     
│       ├── functions.py
│       └── queries.py
```

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone git@github.com:bfreiheit/analysis_collection.git
cd analysis_collection
```
### 2. (Optional) Set up a virtual environment
It is recommended creating a single virtual environment at the top level:

```bash
python -m venv .venv
source .venv/bin/activate
```
### 3. Install project dependencies
Each project contains its own dependencies.
Navigate into the travel_tide directory and install them:

```bash
cd travel_tide
make install
```
### 4. (Optional) Develop mode
To make your project importable and editable as a package:

```bash
make develop
```
This runs pip install -e ., so changes in the travel_tide source code will be immediately reflected.

Available Makefile commands
Once you are inside travel_tide/, you can use the following:

make install — Install dependencies from requirements.txt.

make develop — Install the project in editable mode (pip install -e .).

make notebook — Launch a Jupyter Notebook.

make clean — Remove all __pycache__ directories.

make freeze — Show currently installed packages.

### Notes
Each subproject (travel_tide, etc.) can have its own Makefile, setup.py, and dependencies.

Adjust PYTHON and PIP paths inside the Makefile if you're on MacOS or Linux (../.venv/bin/... instead of ../.venv/Scripts/...).
