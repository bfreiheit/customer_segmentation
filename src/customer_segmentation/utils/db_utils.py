import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(override=True)


def read_from_db(model_name: str) -> pd.DataFrame:
    """
    load the sql file <model_name>.sql from sql/ directory
    and load data into a pandas.DataFrame.
    """
    # load SQL from resource
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, os.path.pardir, "sql")
    sql_path = os.path.join(data_dir, f"{model_name}.sql")

    with open(sql_path, encoding="utf-8") as f:
        query = f.read()

    conn_str = (
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
        f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/TravelTide"
    )
    engine = create_engine(conn_str)

    with engine.connect() as connection:
        return pd.read_sql(query, connection)
