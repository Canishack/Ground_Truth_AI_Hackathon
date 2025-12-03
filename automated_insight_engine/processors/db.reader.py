import sqlite3
import pandas as pd
from typing import Tuple, Dict, Any


def read_sqlite_table(path: str, table_name: str):
    conn = sqlite3.connect(path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM `{table_name}`", conn)
    finally:
        conn.close()
    return df
