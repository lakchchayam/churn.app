# Usage Guide

1. Prepare data with required columns: user_id, last_login, num_sessions, revenue, support_tickets, label.
2. Train model:
   ```bash
   python src/train.py --input data/sample_customers.csv --model models/churn_model.pkl --metrics metrics.json
   ```
3. Predict from CLI:
   ```bash
   python src/predict.py data/sample_customers.csv --model models/churn_model.pkl --output preds.csv
   ```
4. Run Streamlit dashboard:
   ```bash
   streamlit run app/streamlit_app.py
   ```
5. In the app: upload CSV -> preview -> predict -> explain -> view charts -> use what-if sliders.
6. Set `OPENAI_API_KEY` in environment to enable LLM explanations.

