from __future__ import annotations

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

REQUIRED_COLUMNS = ["user_id", "last_login", "num_sessions", "revenue", "support_tickets", "label"]


def validate_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        available = list(df.columns)
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns in your CSV: {available}\n"
            f"Required columns: {REQUIRED_COLUMNS}\n"
            f"Please ensure your CSV has these exact column names."
        )


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)
    out = df.copy()
    # Type conversions
    out["user_id"] = out["user_id"].astype(str)
    out["num_sessions"] = pd.to_numeric(out["num_sessions"], errors="coerce").fillna(0).astype(int)
    out["revenue"] = pd.to_numeric(out["revenue"], errors="coerce").fillna(0.0)
    out["support_tickets"] = pd.to_numeric(out["support_tickets"], errors="coerce").fillna(0).astype(int)

    # Dates - normalize to timezone-naive
    if not is_datetime(out["last_login"]):
        out["last_login"] = pd.to_datetime(out["last_login"], errors="coerce")
    
    # Remove timezone info completely
    if out["last_login"].dt.tz is not None:
        out["last_login"] = out["last_login"].dt.tz_convert("UTC").dt.tz_localize(None)
    else:
        # Already naive, but ensure it's truly naive
        out["last_login"] = pd.to_datetime(out["last_login"], errors="coerce").dt.tz_localize(None)
    
    # Fill missing with naive UTC now
    naive_now = pd.Timestamp.now(tz=None)
    out["last_login"] = out["last_login"].fillna(naive_now)

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

