import os
from typing import Optional

import pandas as pd


def read_or_write_csv(
    file_name: str, df: Optional[pd.DataFrame] = None, to_read: bool = False
) -> Optional[pd.DataFrame]:
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, os.path.pardir, "data")
    data_path = os.path.join(data_dir, file_name)

    if to_read:
        return pd.read_csv(data_path, encoding="utf-8-sig", sep=";")
    else:
        if df is not None:
            df.to_csv(data_path, index=False, encoding="utf-8-sig", sep=";")
        else:
            raise ValueError("DataFrame must be provided when writing.")
