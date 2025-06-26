import os
from dotenv import load_dotenv
import importlib
import importlib.resources as resources

from typing import Callable
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 

load_dotenv(override=True)

# ----------------- data import

def read_from_db(model_name: str) -> pd.DataFrame:
    """
    load the sql file <model_name>.sql from sql/ directory 
    and load data into a pandas.DataFrame.
    """
    # load SQL from resource 
    sql_path = resources.files('customer_segmentation.utils').joinpath(
        f'sql/{model_name}.sql'
    )
    with sql_path.open(encoding='utf-8') as f:
        query = f.read()
    
    conn_str = (
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
        f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/TravelTide"
    )
    engine = create_engine(conn_str)
   
    with engine.connect() as connection:
        return pd.read_sql(query, connection)


# --------------------- preprocessing

def get_binary_columns(df: pd.DataFrame) -> list:
    binarry_cols = []
    for col in df.columns:
        if df[col].nunique() == 2 and set(df[col].unique()) == {0, 1}:
            binarry_cols.append(col)
    return binarry_cols

def find_outliers(df, column):
    mean = df[column].mean()
    std = df[column].std()
    cut_off = std * 3
    lower, upper = mean - cut_off, mean + cut_off
    new_df = df[(df[column] < upper) & (df[column] > lower)]
    return new_df

def normalize_per_month(df, cols, time_column = 'month_active'):
    for col in cols:
        new_col = f"{col}_per_month"
        df[new_col] = df[col] / df[time_column].replace(0, np.nan)
    return df

# ------------------- plot functions 

def plot_time_series(df: pd.DataFrame, x: str, y: list, n_cols = 2) -> None:
   
    n_rows = (len(y) + n_cols - 1) // n_cols

    _, axes = plt.subplots(n_rows, n_cols, figsize=(len(y) + 10, len(y) + 8)) 
    axes = axes.flatten()

    for i, col_name in enumerate(y):
            sns.lineplot(data = df, x = x, y = col_name, ax = axes[i])
            axes[i].set_title(f"{col_name}")
            axes[i].set_xlabel("")
            axes[i].set_ylabel("")
    plt.tight_layout()
    plt.show()

def plot_univariate_series(df: pd.DataFrame, metrics: list, n_cols: int = 4, plot_type: Callable = sns.boxplot) -> None:

    n_rows = (len(metrics) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize = (13, n_rows * 2))
    axes = axes.flatten() 
    for i, col_name in enumerate(metrics):
        df_filtered = df[df[col_name] > 0]
        plot_type(data = df_filtered, x = col_name, ax = axes[i])
        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

    plt.tight_layout()
    plt.show()


def plot_bivariate_series(df: pd.DataFrame, category:str, metrics: list, n_cols: int = 4, plot_type: Callable = sns.barplot) -> None:

    n_rows = (len(metrics) + n_cols - 1) // n_cols

    _, axes = plt.subplots(n_rows, n_cols, figsize = (13, n_rows * 2))
    axes = axes.flatten() 
    for i, col_name in enumerate(metrics):
        plot_type(data = df, x = category, y = col_name, ax = axes[i])
        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")
    plt.tight_layout()
    plt.show()