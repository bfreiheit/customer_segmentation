import os
from dotenv import load_dotenv
import importlib

from typing import Callable
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 

from travel_tide.utils import queries
importlib.reload(queries)

load_dotenv(override=True)

def read_from_db(query):
    conn_str = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/TravelTide"
    engine = create_engine(conn_str)
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

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
#TODO: bug in size
def plot_time_series(df: pd.DataFrame, x: str, y: list, n_cols = 2) -> None:
   
    size = [(i, j) for i in range(len(y)-1) for j in range(len(y)-1) if j <= 1 and i <= 1]    
    rows = len(size) // n_cols

    _, axes = plt.subplots(rows, n_cols, figsize=(len(size)**2, len(size)+2))  
  
    for s, col in zip(size, y):
        i, j = s      
        sns.lineplot(data=df, x=x, y=col, ax=axes[i, j])
        axes[i, j].set_title(f'{col} | {x}')
        axes[i, j].xaxis.set_major_locator(mdates.MonthLocator(interval=2)) 
        axes[i, j].xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
        axes[i, j].set_xlabel("")
       
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