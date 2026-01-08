import json
import os
from typing import List

import pandas as pd
import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Json


SHEET_TABLE = "maker_sheet_rows"


def _get_database_url() -> str:
    for env_key in (
        "DATABASE_URL",
        "POSTGRES_URL",
        "KUEST_DATABASE_URL",
        "KUEST_MAKER_DATABASE_URL",
    ):
        value = os.getenv(env_key)
        if value:
            return value
    raise ValueError("DATABASE_URL environment variable is not set")


def _connect():
    return psycopg.connect(_get_database_url())


def ensure_schema(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SHEET_TABLE} (
                id BIGSERIAL PRIMARY KEY,
                sheet_name TEXT NOT NULL,
                row_data JSONB NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """
        )
        cur.execute(
            f"CREATE INDEX IF NOT EXISTS idx_{SHEET_TABLE}_sheet_name ON {SHEET_TABLE}(sheet_name);"
        )


def _df_to_records(df: pd.DataFrame) -> List[dict]:
    if df is None or df.empty:
        return []
    # Ensure all values are JSON-serializable (no numpy types/NaN).
    df = df.where(pd.notna(df), None)
    return json.loads(df.to_json(orient="records"))


def replace_sheet_rows(sheet_name: str, df: pd.DataFrame) -> None:
    records = _df_to_records(df)
    with _connect() as conn:
        ensure_schema(conn)
        with conn.cursor() as cur:
            cur.execute(
                f"DELETE FROM {SHEET_TABLE} WHERE sheet_name = %s",
                (sheet_name,),
            )
            if records:
                cur.executemany(
                    f"INSERT INTO {SHEET_TABLE} (sheet_name, row_data) VALUES (%s, %s)",
                    [(sheet_name, Json(row)) for row in records],
                )


def fetch_sheet_df(sheet_name: str) -> pd.DataFrame:
    with _connect() as conn:
        ensure_schema(conn)
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                f"SELECT row_data FROM {SHEET_TABLE} WHERE sheet_name = %s",
                (sheet_name,),
            )
            records = [row["row_data"] for row in cur.fetchall()]
    return pd.DataFrame(records)
