import inspect
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

    # which parameters are accepted per plot type
    sig = inspect.signature(plot_type)
    accepted_params = sig.parameters.keys()

    for i, col_name in enumerate(metrics):
        df_filtered = df[df[col_name] > 0]

        plot_kwargs = {"data": df_filtered, "x": col_name, "ax": axes[i]}
        if "kde" in accepted_params:
            plot_kwargs["kde"] = set_kde
        if "bins" in accepted_params:
            plot_kwargs["bins"] = set_bins

        plot_type(**plot_kwargs)

        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

    # removes not used axes
    for j in range(len(metrics), len(axes)):
        fig.delaxes(axes[j])

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

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height))
    axes = axes.flatten()

    for i, col_name in enumerate(metrics):
        plot_kwargs = {"data": df, "ax": axes[i]}
        if swap_axes:
            plot_kwargs["x"] = col_name
            plot_kwargs["y"] = category
        else:
            plot_kwargs["x"] = category
            plot_kwargs["y"] = col_name

        plot_type(**plot_kwargs)

        axes[i].set_title(f"{col_name}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

    # removes not used axes
    for j in range(len(metrics), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def plot_relation_series(
    df: pd.DataFrame,
    x: list,
    y: list,
    n_cols: int = 4,
    plot_type: Callable = sns.scatterplot,
    fig_width: int = 13,
    fig_height: int = 26,
) -> None:
    n_rows = (len(x) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height))
    axes = axes.flatten()

    for i, (x_, y_) in enumerate(zip(x, y)):
        plot_kwargs = {"data": df, "ax": axes[i]}
        plot_kwargs["x"] = x_
        plot_kwargs["y"] = y_

        plot_type(**plot_kwargs)

        axes[i].set_title(f"{x_}")
        axes[i].set_xlabel(f"{x_}")
        axes[i].set_ylabel(f"{y_}")

    # removes not used axes
    for j in range(len(x), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
