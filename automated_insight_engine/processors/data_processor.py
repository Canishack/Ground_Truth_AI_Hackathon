import pandas as pd
import sqlite3
import sqlparse
from typing import Tuple, Dict, Any


def _summarize_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    numeric = df.select_dtypes(include="number")
    return {
        "columns": list(df.columns),
        "row_count": int(len(df)),
        "missing_values": df.isna().sum().to_dict(),
        "numeric_summary": numeric.describe().to_dict(),
        "sample_rows": df.head(5).to_dict(orient="records")
    }


def process_csv(path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    df = pd.read_csv(path)
    return df, _summarize_dataframe(df)


def process_sql(path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    # Load SQL dump into in-memory sqlite and read first table
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        sql_text = fh.read()

    conn = sqlite3.connect(":memory:")
    statements = sqlparse.split(sql_text)
    for stmt in statements:
        try:
            conn.execute(stmt)
        except Exception:
            # ignore statements that fail (eg. non-INSERT statements for other DB engines)
            continue

    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    if not tables:
        raise RuntimeError("No table found in SQL dump")
    table_name = tables[0][0]
    df = pd.read_sql_query(f"SELECT * FROM `{table_name}`", conn)
    conn.close()
    return df, _summarize_dataframe(df)


def process_db(path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    conn = sqlite3.connect(path)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    if not tables:
        conn.close()
        raise RuntimeError("No table found in DB file")
    table_name = tables[0][0]
    df = pd.read_sql_query(f"SELECT * FROM `{table_name}`", conn)
    conn.close()
    return df, _summarize_dataframe(df)
