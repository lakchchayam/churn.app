import os
import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to path for Streamlit Cloud
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import streamlit as st
import plotly.express as px

from src import data_ingest, features, predict, llm_explain, actions

st.set_page_config(page_title="Churn Intelligence Platform", layout="wide")


@st.cache_data(show_spinner=False)
def load_sample():
    sample_path = Path("data/sample_customers.csv")
    return pd.read_csv(sample_path)


@st.cache_resource(show_spinner=False)
def load_model():
    model_path = Path("models/churn_model.pkl")
    if not model_path.exists():
        st.warning("Model not found. Training model now...")
        try:
            from src import train
            train.train_model(
                input_csv="data/sample_customers.csv",
                model_path=str(model_path),
                metrics_path="metrics.json"
            )
            st.success("Model trained successfully!")
        except Exception as e:
            st.error(f"Could not train model: {e}")
            return None
    
    try:
        return predict.load_model(model_path)
    except Exception as e:
        st.warning(f"Model loading failed (version mismatch): {e}. Retraining...")
        try:
            from src import train
            train.train_model(
                input_csv="data/sample_customers.csv",
                model_path=str(model_path),
                metrics_path="metrics.json"
            )
            return predict.load_model(model_path)
        except Exception as retrain_error:
            st.error(f"Could not retrain model: {retrain_error}")
            return None


@st.cache_data(show_spinner=False)
def prepare_features(df: pd.DataFrame):
    return features.build_features(df)


@st.cache_data(show_spinner=False)
def run_predictions(df: pd.DataFrame, _model):
    if _model is None:
        out = df[["user_id"]].copy()
        out["churn_prob"] = 0.5
        return out
    return predict.predict_df(df, _model)


@st.cache_data(show_spinner=False)
def risk_buckets(preds: pd.DataFrame):
    bins = [0, 0.33, 0.66, 1.0]
    labels = ["Low", "Medium", "High"]
    preds = preds.copy()
    preds["risk"] = pd.cut(preds["churn_prob"], bins=bins, labels=labels, include_lowest=True)
    return preds


def section_header(title):
    st.markdown(f"### {title}")


st.title("Churn Intelligence Platform")
st.write("Upload data, predict churn, explain drivers, and simulate interventions.")

with st.sidebar:
    st.header("Demo")
    if st.button("Load Sample Data"):
        st.session_state["uploaded_df"] = load_sample()
        st.success("Loaded sample data.")
    st.info("Columns required: user_id, last_login, num_sessions, revenue, support_tickets, label (optional for inference)")
    st.markdown("---")
    st.markdown("**Built by Lakshyam** 🚀")

section_header("1) Upload CSV")
upload = st.file_uploader("Upload customer CSV", type=["csv"])
if upload:
    df = pd.read_csv(upload)
    st.session_state["uploaded_df"] = df

if "uploaded_df" not in st.session_state:
    st.stop()

raw_df = st.session_state["uploaded_df"]

section_header("2) Preview")
st.dataframe(raw_df.head())

section_header("3) Predict Churn")
try:
    cleaned = data_ingest.clean_dataframe(raw_df)
    model = load_model()
    # Pass cleaned dataframe (with all columns) to predict_df, not feature dataframe
    preds = run_predictions(cleaned, model)
    preds_with_risk = risk_buckets(preds)
    st.dataframe(preds_with_risk)
except Exception as e:  # noqa: BLE001
    error_msg = str(e)
    st.error(f"Error during prediction: {error_msg}")
    
    # Show helpful message about CSV format
    st.info("""
    **📋 Required CSV Format:**
    
    Your CSV must have these exact column names:
    - `user_id` (string)
    - `last_login` (date: YYYY-MM-DD)
    - `num_sessions` (number)
    - `revenue` (number)
    - `support_tickets` (number)
    - `label` (0 or 1, optional for inference)
    
    **Current CSV columns:** """ + ", ".join(raw_df.columns.tolist()))
    st.stop()

section_header("4) Explain & Recommend")
selected_user = st.selectbox("Select user_id to explain", preds_with_risk["user_id"].astype(str))
if st.button("Generate Explanation"):
    row = preds_with_risk[preds_with_risk["user_id"].astype(str) == str(selected_user)].iloc[0]
    driver_cols = ["recency", "session_rate", "support_rate", "revenue_bin"]
    drivers = row[driver_cols].to_dict()
    action = actions.recommend_action(row)
    llm_payload = llm_explain.build_llm_payload(
        user_id=row["user_id"],
        churn_prob=row["churn_prob"],
        top_drivers=drivers,
        action=action,
    )
    st.json(llm_payload)

section_header("5) Dashboard")
chart_df = preds_with_risk.copy()
count_fig = px.histogram(chart_df, x="risk")
density_fig = px.histogram(chart_df, x="churn_prob", nbins=20, title="Churn probability distribution")
col1, col2 = st.columns(2)
col1.plotly_chart(count_fig, use_container_width=True)
col2.plotly_chart(density_fig, use_container_width=True)

section_header("6) What-If Simulator")
sim_user = st.selectbox("Pick a user to simulate", preds_with_risk["user_id"].astype(str))
row = cleaned[cleaned["user_id"].astype(str) == str(sim_user)].iloc[0].copy()

# Safe defaults for sliders
num_sessions_val = int(row.get("num_sessions", 0)) if pd.notna(row.get("num_sessions")) else 0
support_val = int(row.get("support_tickets", 0)) if pd.notna(row.get("support_tickets")) else 0
revenue_val = float(row.get("revenue", 0)) if pd.notna(row.get("revenue")) else 0.0

sim_num_sessions = st.slider("num_sessions", 0, 200, num_sessions_val)
sim_support = st.slider("support_tickets", 0, 10, support_val)
sim_revenue = st.slider("revenue", 0, 1000, int(revenue_val))

if st.button("Recompute Churn"):
    sim_df = row.to_frame().T
    sim_df["num_sessions"] = sim_num_sessions
    sim_df["support_tickets"] = sim_support
    sim_df["revenue"] = float(sim_revenue)
    # Ensure all required columns are present
    if "last_login" not in sim_df.columns or pd.isna(sim_df["last_login"].iloc[0]):
        sim_df["last_login"] = pd.Timestamp.now()
    sim_pred = run_predictions(sim_df, model).iloc[0]
    st.success(f"New churn probability: {sim_pred['churn_prob']:.2f}")
    # Get action from cleaned dataframe row, not feature dataframe
    sim_action = actions.recommend_action(sim_df.iloc[0])
    st.json(sim_action)

st.markdown("---")
st.markdown("### 💡 What is this platform?")
st.markdown("""
**Churn Intelligence Platform** is an ML-powered solution that helps businesses:

- **🔮 Predict Churn Risk**: Uses Gradient Boosting ML model to predict which customers are likely to churn
- **🤖 AI Explanations**: LLM-powered natural language explanations of why customers might churn
- **⚡ Actionable Insights**: Rule-based + AI recommendations for retention strategies
- **📊 Interactive Dashboard**: Visualize churn risk distribution and customer segments
- **🎯 What-If Simulator**: Test different scenarios (sessions, support tickets, revenue) to see impact on churn probability

**Use Cases:**
- **Customer Success Teams**: Identify at-risk customers and prioritize outreach
- **Growth Teams**: Understand churn drivers and optimize retention campaigns
- **Product Teams**: Discover feature gaps and engagement patterns
- **Business Analysts**: Make data-driven decisions on customer retention strategies

**Built by Lakshyam** 🚀
""")
st.markdown("---")
st.caption("Churn Intelligence Platform · Powered by ML + LLM · Built by Lakshyam · Streamlit")

