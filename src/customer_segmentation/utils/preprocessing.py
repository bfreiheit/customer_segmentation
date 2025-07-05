import numpy as np
import pandas as pd
from typing import Tuple
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler


def get_binary_columns(df: pd.DataFrame) -> list:
    binarry_cols = []
    for col in df.columns:
        if df[col].nunique() == 2 and set(df[col].unique()) == {0, 1}:
            binarry_cols.append(col)
    return binarry_cols


def missing_data(df: pd.DataFrame) -> pd.DataFrame:
    total = df.isnull().sum().sort_values(ascending=False)
    total = total[total.apply(lambda x: x > 0)]

    Percentage = (df.isnull().sum() / df.isnull().count() * 100).sort_values(
        ascending=False
    )
    Percentage = Percentage[Percentage.apply(lambda x: x > 0.00)]
    return pd.concat([total, Percentage], axis=1, keys=["Total", "Percentage"])


def apply_PCA(df: pd.DataFrame, features: list, score_name: str, n_components: int = 1) -> Tuple[pd.DataFrame, tuple]:
    pca_info = []
    pca = PCA(n_components=n_components)
    score = pca.fit_transform(df[features])

    pca_info = (pca.explained_variance_ratio_.flatten(), pca.components_.flatten())   
    df[score_name] = score
    return df, pca_info
