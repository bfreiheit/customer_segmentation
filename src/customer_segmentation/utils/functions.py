import importlib.resources as resources
import os
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sqlalchemy import create_engine

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
    # 1. check skewness
    skewness = df[features].skew(numeric_only=True)
    highly_skewed = skewness[np.abs(skewness) > 0.75].index.to_list()
    lowly_skewed = list(set(features) - set(highly_skewed))

    # 2. define transformations
    transformers = ColumnTransformer(
        transformers=[
            (
                "log+scale",
                make_pipeline(
                    FunctionTransformer(np.log1p, feature_names_out="one-to-one"),
                    StandardScaler(),
                ),
                highly_skewed,
            ),
            ("scale", StandardScaler(), lowly_skewed),
        ]
    )

    # 3. transform data
    X_transformed = transformers.fit_transform(df[features])

    # 4. PCA
    pca = PCA(n_components=1)
    score = pca.fit_transform(X_transformed)

    # 5. attach score to df
    df[score_name] = score
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
    df: pd.DataFrame,
    metrics: list,
    n_cols: int = 4,
    set_kde: bool = True,
    set_bins: int = 20,
    plot_type: Callable = sns.boxplot,
) -> None:

    n_rows = (len(metrics) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, n_rows * 2))
    axes = axes.flatten()
    for i, col_name in enumerate(metrics):
        df_filtered = df[df[col_name] > 0]
        plot_type(data=df_filtered, x=col_name, ax=axes[i], kde=set_kde, bins=set_bins)
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
    swap_axes: bool = False,
    fig_width: int = 13,
    fig_height: int = 26,
) -> None:

    n_rows = (len(metrics) + n_cols - 1) // n_cols

    _, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height))
    axes = axes.flatten()
    for i, col_name in enumerate(metrics):
        if swap_axes:
            plot_type(data=df, x=col_name, y=category, ax=axes[i])
        else:
            plot_type(data=df, x=category, y=col_name, ax=axes[i])
        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")
    plt.tight_layout()
    plt.show()
