from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import joblib

from src import data_ingest, features


def load_model(model_path: Path):
    return joblib.load(model_path)


def predict_df(df: pd.DataFrame, model) -> pd.DataFrame:
    feat = features.build_features(df)
    X = feat.drop(columns=["user_id"])
    churn_prob = model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else model.predict(X)
    out = feat.copy()
    out["churn_prob"] = churn_prob
    return out[["user_id", "recency", "session_rate", "support_rate", "revenue_bin", "churn_prob"]]


def predict_file(input_csv: str, model_path: str) -> pd.DataFrame:
    model = load_model(Path(model_path))
    df = data_ingest.ingest_csv(input_csv)
    return predict_df(df, model)


def main():
    parser = argparse.ArgumentParser(description="Predict churn probabilities")
    parser.add_argument("input_csv", help="Input CSV file")
    parser.add_argument("--model", default="models/churn_model.pkl", help="Model path")
    parser.add_argument("--output", help="Optional output CSV")
    args = parser.parse_args()

    preds = predict_file(args.input_csv, args.model)
    if args.output:
        preds.to_csv(args.output, index=False)
    else:
        print(preds.to_csv(index=False))


if __name__ == "__main__":
    main()

