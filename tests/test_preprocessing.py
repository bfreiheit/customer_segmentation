import numpy as np
import pandas as pd
import pandas.testing as pdt
import pytest

from customer_segmentation.utils import preprocessing


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "col1": np.repeat([0, 1], [5, 5]),
            "col2": [x if x < 9 else np.nan for x in range(10)],
            "col3": [x if x % 2 == 0 else np.nan for x in range(10)],
        }
    )


def test_get_binary_columns(df: pd.DataFrame) -> None:
    binarry_cols = []
    for col in df.columns:
        if df[col].nunique() == 2 and set(df[col].unique()) == {0, 1}:
            binarry_cols.append(col)

    assert binarry_cols == ["col1"]


def test_missing_data(df: pd.DataFrame) -> None:
    total = df.isnull().sum().sort_values(ascending=False)
    total = total[total.apply(lambda x: x > 0)]

    Percentage = (df.isnull().sum() / df.isnull().count() * 100).sort_values(
        ascending=False
    )
    Percentage = Percentage[Percentage.apply(lambda x: x > 0.00)]

    result = pd.concat([total, Percentage], axis=1, keys=["Total", "Percentage"])

    data = {"Total": [5, 1], "Percentage": [50.0, 10.0]}
    index_labels = ["col3", "col2"]

    expected = pd.DataFrame(data, index=index_labels)

    pdt.assert_frame_equal(result, expected)


def test_apply_PCA():
    df = pd.DataFrame({"feat1": [1, 2, 3, 4], "feat2": [4, 5, 6, 7]})

    result_df, pca_info = preprocessing.apply_PCA(
        df.copy(), features=["feat1", "feat2"], score_name="PCA_Score", n_components=1
    )

    # Test 1: new column exist
    assert "PCA_Score" in result_df.columns

    # Test 2: length of column correct
    assert len(result_df["PCA_Score"]) == len(df)

    # Test 3: pca_info is tuple with 2 arrays
    assert isinstance(pca_info, tuple)
    assert len(pca_info) == 2
    assert isinstance(pca_info[0], np.ndarray)
    assert isinstance(pca_info[1], np.ndarray)

    # Test 4: explained_variance_ratio sum to <= 1
    assert np.all(pca_info[0] <= 1.0)
