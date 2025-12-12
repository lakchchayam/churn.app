from __future__ import annotations

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

REQUIRED_COLUMNS = ["user_id", "last_login", "num_sessions", "revenue", "support_tickets", "label"]

# Flexible column mapping - common variations
COLUMN_MAPPINGS = {
    "user_id": ["user_id", "userid", "user", "id", "customer_id", "customerid", "customer", "client_id", "customerid", "customer_id", "clientid"],
    "last_login": ["last_login", "lastlogin", "last_login_date", "login_date", "last_activity", "last_activity_date", "date", "last_interaction", "lastinteraction", "interaction_date", "activity_date"],
    "num_sessions": ["num_sessions", "numsessions", "sessions", "session_count", "total_sessions", "activity_count", "usage_frequency", "usagefrequency", "frequency", "engagement", "activity"],
    "revenue": ["revenue", "total_revenue", "revenue_total", "amount", "value", "spend", "lifetime_value", "ltv", "total_spend", "totalspend", "payment", "billing"],
    "support_tickets": ["support_tickets", "supporttickets", "tickets", "ticket_count", "support_count", "complaints", "issues", "support_calls", "supportcalls", "calls", "support_requests"],
    "label": ["label", "churn", "churned", "is_churn", "churn_label", "target", "y", "churn_status", "churnstatus"]
}


def map_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Automatically map common column names to required format"""
    df_mapped = df.copy()
    mapping_applied = {}
    
    def normalize_name(name: str) -> str:
        """Normalize column name for comparison"""
        return str(name).lower().strip().replace(" ", "_").replace("-", "_")
    
    for required_col, possible_names in COLUMN_MAPPINGS.items():
        if required_col not in df_mapped.columns:
            # Try to find matching column (case-insensitive, space/dash normalized)
            for col in df_mapped.columns:
                col_normalized = normalize_name(col)
                possible_normalized = [normalize_name(name) for name in possible_names]
                
                if col_normalized in possible_normalized:
                    df_mapped[required_col] = df_mapped[col]
                    mapping_applied[required_col] = col
                    break
    
    return df_mapped, mapping_applied


def validate_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Validate and auto-map columns"""
    df_mapped, mapping = map_columns(df)
    
    missing = [c for c in REQUIRED_COLUMNS if c not in df_mapped.columns]
    if missing:
        available = list(df.columns)
        # Show what was mapped
        mapped_info = f"Mapped: {mapping}" if mapping else "No columns were auto-mapped."
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns in your CSV: {available}\n"
            f"Required columns: {REQUIRED_COLUMNS}\n"
            f"{mapped_info}\n"
            f"Couldn't auto-map: {missing}\n"
            f"Please ensure your CSV has columns that match: user_id/customer_id, last_login/last_interaction, num_sessions/usage_frequency, revenue/total_spend, support_tickets/support_calls, label/churn"
        )
    
    return df_mapped, mapping


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out, mapping = validate_columns(df)
    out = out.copy()
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

