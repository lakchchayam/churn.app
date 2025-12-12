from __future__ import annotations

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

REQUIRED_COLUMNS = ["user_id", "last_login", "num_sessions", "revenue", "support_tickets", "label"]


def validate_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)
    out = df.copy()
    # Type conversions
    out["user_id"] = out["user_id"].astype(str)
    out["num_sessions"] = pd.to_numeric(out["num_sessions"], errors="coerce").fillna(0).astype(int)
    out["revenue"] = pd.to_numeric(out["revenue"], errors="coerce").fillna(0.0)
    out["support_tickets"] = pd.to_numeric(out["support_tickets"], errors="coerce").fillna(0).astype(int)

    # Dates
    if not is_datetime(out["last_login"]):
        out["last_login"] = pd.to_datetime(out["last_login"], errors="coerce")
    # Normalize timezone to naive UTC to avoid tz-aware vs tz-naive subtraction
    if hasattr(out["last_login"].dt, "tz") and out["last_login"].dt.tz is not None:
        out["last_login"] = out["last_login"].dt.tz_convert("UTC").dt.tz_localize(None)
    else:
        out["last_login"] = out["last_login"].dt.tz_localize(None)
    out["last_login"] = out["last_login"].fillna(pd.Timestamp.utcnow().tz_localize(None))

    # Labels optional for inference: fill with 0 if missing
    if out["label"].isna().any():
        out["label"] = out["label"].fillna(0).astype(int)
    else:
        out["label"] = out["label"].astype(int)

    return out


def save_parquet(df: pd.DataFrame, path: str) -> None:
    df.to_parquet(path, index=False)


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def ingest_csv(path: str, parquet_path: str | None = None) -> pd.DataFrame:
    df = load_csv(path)
    cleaned = clean_dataframe(df)
    if parquet_path:
        save_parquet(cleaned, parquet_path)
    return cleaned

