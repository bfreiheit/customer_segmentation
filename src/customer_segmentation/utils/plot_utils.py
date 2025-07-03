from typing import Callable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
