import os
from dotenv import load_dotenv
import importlib.resources as resources

from typing import Callable
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

load_dotenv(override=True)

# ----------------- data import


def read_from_db(model_name: str) -> pd.DataFrame:
    """
    load the sql file <model_name>.sql from sql/ directory
    and load data into a pandas.DataFrame.
    """
    # load SQL from resource
    sql_path = resources.files("customer_segmentation.utils").joinpath(
        f"sql/{model_name}.sql"
    )
    with sql_path.open(encoding="utf-8") as f:
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


def missing_data(df):
    total = df.isnull().sum().sort_values(ascending=False)
    total = total[total.apply(lambda x: x > 0)]

    Percentage = (df.isnull().sum() / df.isnull().count() * 100).sort_values(
        ascending=False
    )
    Percentage = Percentage[Percentage.apply(lambda x: x > 0.00)]
    return pd.concat([total, Percentage], axis=1, keys=["Total", "Percentage"])

def PCA_pipeline(df: pd.DataFrame, features: list, score_name: str) -> pd.DataFrame:
    # 1. standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    # 2. apply PCA to subset
    pca = PCA(n_components=1)
    df[score_name] = pca.fit_transform(X_scaled)
    return df

# ------------------- plot functions


def plot_time_series(df: pd.DataFrame, x: str, y: list, n_cols=2) -> None:

    n_rows = (len(y) + n_cols - 1) // n_cols

    _, axes = plt.subplots(n_rows, n_cols, figsize=(len(y) + 10, len(y) + 8))
    axes = axes.flatten()

    for i, col_name in enumerate(y):
        sns.lineplot(data=df, x=x, y=col_name, ax=axes[i])
        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")
    plt.tight_layout()
    plt.show()


def plot_univariate_series(
    df: pd.DataFrame, metrics: list, n_cols: int = 4, plot_type: Callable = sns.boxplot
) -> None:

    n_rows = (len(metrics) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(13, n_rows * 2))
    axes = axes.flatten()
    for i, col_name in enumerate(metrics):
        df_filtered = df[df[col_name] > 0]
        plot_type(data=df_filtered, x=col_name, ax=axes[i])
        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

    plt.tight_layout()
    plt.show()


def plot_bivariate_series(
    df: pd.DataFrame,
    category: str,
    metrics: list,
    n_cols: int = 4,
    plot_type: Callable = sns.barplot,
) -> None:

    n_rows = (len(metrics) + n_cols - 1) // n_cols

    _, axes = plt.subplots(n_rows, n_cols, figsize=(13, n_rows * 2))
    axes = axes.flatten()
    for i, col_name in enumerate(metrics):
        plot_type(data=df, x=category, y=col_name, ax=axes[i])
        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")
    plt.tight_layout()
    plt.show()
