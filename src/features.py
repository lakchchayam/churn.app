import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Ensure last_login is timezone-naive
    if "last_login" in out.columns:
        if out["last_login"].dt.tz is not None:
            out["last_login"] = out["last_login"].dt.tz_convert("UTC").dt.tz_localize(None)
        else:
            # Already naive, ensure it stays naive
            out["last_login"] = pd.to_datetime(out["last_login"], errors="coerce").dt.tz_localize(None)

    # Create NOW as timezone-naive (use now() instead of utcnow())
    now = pd.Timestamp.now(tz=None)

    # recency calculation
    out["recency"] = (now - out["last_login"]).dt.days.clip(lower=0)

    # Defensive divides
    out["session_rate"] = out["num_sessions"] / (out["recency"] + 1)
    out["support_rate"] = out["support_tickets"] / (out["recency"] + 1)

    # Revenue binning
    out["revenue_bin"] = (
        pd.qcut(out["revenue"], q=4, labels=False, duplicates="drop")
        .fillna(0)
        .astype(int)
    )

    feature_cols = ["user_id", "recency", "session_rate", "support_rate", "revenue_bin"]
    return out[feature_cols]


def split_features_labels(df: pd.DataFrame):
    if "label" not in df.columns:
        raise ValueError("label column required for training")

    feats = build_features(df)
    X = feats.drop(columns=["user_id"])
    y = df["label"].astype(int)
    return X, y
