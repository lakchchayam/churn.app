# Architecture

## Data Flow
- CSV ingest -> validation -> type casting -> parquet optional.
- Feature builder computes recency, session_rate, support_rate, revenue_bin.
- Model predicts churn probability -> risk buckets -> UI.

## Model Pipeline
1. Ingest CSV via `data_ingest.py`
2. Feature engineering in `features.py`
3. Train `GradientBoostingClassifier` in `train.py`
4. Save model to `models/churn_model.pkl` and metrics JSON
5. Predict via `predict.py` using the same feature builder

## LLM Module
- System prompt + few-shot examples
- Input: user_id, churn_prob, top_drivers, rule-based action
- Output JSON with explanation and recommended action (offline fallback when no API key)

## Action Engine
- Rule-based priority:
  - recency > 45 -> high-priority reactivation
  - support_tickets > 3 -> intervention
  - low revenue_bin -> discount trigger
  - else -> defer to LLM suggestion

