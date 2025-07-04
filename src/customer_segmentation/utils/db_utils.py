import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv(override=True)


def get_engine(db_mode: str = "remote") -> "Engine":

    if db_mode == "remote":
        user = os.getenv("DB_USER_REMOTE")
        password = os.getenv("DB_PASSWORD_REMOTE")
        host = os.getenv("DB_HOST_REMOTE")
        port = os.getenv("DB_PORT_REMOTE")
        conn_str = f"postgresql://{user}:{password}@{host}:{port}/TravelTide"
    else:
        user = os.getenv("DB_USER_LOCAL")
        password = os.getenv("DB_PASSWORD_LOCAL")
        host = os.getenv("DB_HOST_LOCAL")
        port = os.getenv("DB_PORT_LOCAL")
        conn_str = f"postgresql://{user}:{password}@{host}:{port}/travel_tide"

    return create_engine(conn_str)


def read_sql_file(file_name: str):
    """
    load the sql file <file_name>.sql from sql/ directory
    and load data into a pandas.DataFrame.
    """
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, os.path.pardir, "sql")
    sql_path = os.path.join(data_dir, f"{file_name}.sql")

    if not os.path.exists(sql_path):
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    with open(sql_path, encoding="utf-8") as f:
        query = f.read()

    return query


def read_from_db_to_df(sql_filename: str, db_mode: str = "remote") -> pd.DataFrame:

    sql = read_sql_file(file_name=sql_filename)

    engine = get_engine(db_mode=db_mode)

    with engine.connect() as connection:
        return pd.read_sql(sql, connection)


def write_from_df_to_db(
    df: pd.DataFrame, tablename: str, db_mode: str = "local"
) -> None:
    engine = get_engine(db_mode=db_mode)

    with engine.connect() as connection:
        df.to_sql(tablename, engine, if_exists="replace", index=False)


def execute_sql(sql_filename: str, db_mode: str = "local") -> None:
    sql = read_sql_file(file_name=sql_filename)

    engine = get_engine(db_mode=db_mode)

    with engine.begin() as conn:  # begin() triggers commit
        conn.execute(text(sql))
        print(f"Successfully executed {sql_filename}.sql")
