import numpy as np
import pandas as pd
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
