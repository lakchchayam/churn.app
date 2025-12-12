from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from src import data_ingest, predict, llm_explain, actions

app = FastAPI(title="Churn Intelligence API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static web files
web_path = Path(__file__).parent.parent / "web"
if web_path.exists():
    app.mount("/static", StaticFiles(directory=str(web_path)), name="static")


def _load_model():
    model_path = Path("models/churn_model.pkl")
    if not model_path.exists():
        return None
    return predict.load_model(model_path)


MODEL = _load_model()


class CustomerRecord(BaseModel):
    user_id: str
    last_login: str
    num_sessions: int
    revenue: float
    support_tickets: int
    label: Optional[int] = Field(default=0, description="Optional; ignored for inference")


class PredictRequest(BaseModel):
    customers: List[CustomerRecord]
    include_explanations: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict_customers(payload: PredictRequest):
    if MODEL is None:
        raise HTTPException(status_code=400, detail="Model not found. Train first via src/train.py.")

    df = pd.DataFrame([c.model_dump() for c in payload.customers])
    try:
        cleaned = data_ingest.clean_dataframe(df)
        preds = predict.predict_df(cleaned, MODEL)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}") from e

    results = []
    merged = cleaned.merge(preds, on="user_id")
    for _, row in merged.iterrows():
        action = actions.recommend_action(row)
        if payload.include_explanations:
            explanation = llm_explain.call_llm(
                user_id=row["user_id"],
                churn_prob=row["churn_prob"],
                top_drivers={
                    "recency": row["recency"],
                    "session_rate": row["session_rate"],
                    "support_rate": row["support_rate"],
                    "revenue_bin": row["revenue_bin"],
                },
                action=action,
            )
        else:
            explanation = llm_explain.build_llm_payload(
                user_id=row["user_id"],
                churn_prob=row["churn_prob"],
                top_drivers={
                    "recency": row["recency"],
                    "session_rate": row["session_rate"],
                    "support_rate": row["support_rate"],
                    "revenue_bin": row["revenue_bin"],
                },
                action=action,
            )
        results.append(explanation)

    return {"results": results}


@app.get("/")
def root():
    index_file = web_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Churn Intelligence API. Use /predict with JSON payload."}

