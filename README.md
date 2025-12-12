# Churn Intelligence Platform

A ready-to-deploy ML + LLM powered platform to predict customer churn, explain risk drivers, and recommend actions. Includes reproducible pipelines, Streamlit dashboard, and what-if simulator.

## Features
- ML churn prediction with Gradient Boosting
- LLM-based natural language explanations and suggested actions
- Rule-based action engine for fast interventions
- Streamlit dashboard with upload, preview, predictions, explanations, charts
- What-if simulator to test retention strategies
- Reproducible training & inference pipelines

## Quickstart (Local)
1. Create virtual env & install deps:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Train model (uses sample data):
   ```bash
   python src/train.py --input data/sample_customers.csv --model models/churn_model.pkl --metrics metrics.json
   ```
3. Run Streamlit app:
   ```bash
   streamlit run app/streamlit_app.py
   ```
4. Run REST API (FastAPI):
   ```bash
   uvicorn api.server:app --reload --port 8000
   ```
   Sample request:
   ```bash
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{
       "include_explanations": true,
       "customers": [{
         "user_id": "U123",
         "last_login": "2024-11-01",
         "num_sessions": 5,
         "revenue": 120,
         "support_tickets": 1,
         "label": 0
       }]
     }'
   ```

## Deploy on Streamlit Cloud
1. Push this repo to GitHub.
2. In Streamlit Cloud, create a new app pointing to `app/streamlit_app.py`.
3. Set environment variables in app settings:
   - `OPENAI_API_KEY` (or compatible LLM key)
4. Deploy; the app will install `requirements.txt` and run.

## Environment Variables
- `OPENAI_API_KEY`: for LLM explanations (required for explanation step; app still works for predictions without it).

## Project Structure
- `app/streamlit_app.py`: Streamlit UI
- `api/server.py`: FastAPI server for programmatic access
- `web/`: Static HTML/CSS/JS UI hitting the same API
- `src/`: pipelines (ingest, features, train, predict, explain, actions)
- `data/sample_customers.csv`: synthetic demo data
- `models/`: trained model artifact destination
- `docs/`: architecture and usage guides

## Screenshots (placeholders)
- Dashboard view: `docs/img/dashboard.png`
- Explanation modal: `docs/img/explanation.png`
- What-if simulator: `docs/img/what_if.png`

## Reproducibility
- Deterministic preprocessing & feature engineering
- CLI-friendly training and inference scripts
- Metrics JSON output for traceability

## License
MIT

