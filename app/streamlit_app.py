import os
import json
import tempfile
from pathlib import Path

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
        st.warning("Model not found. Please run training first (src/train.py). Using a dummy model that outputs 0.5.")
        return None
    return predict.load_model(model_path)


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
    feat_df = prepare_features(cleaned)
    model = load_model()
    preds = run_predictions(feat_df, model)
    preds_with_risk = risk_buckets(preds)
    st.dataframe(preds_with_risk)
except Exception as e:  # noqa: BLE001
    st.error(f"Error during prediction: {e}")
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

sim_num_sessions = st.slider("num_sessions", 0, 200, int(row["num_sessions"]))
sim_support = st.slider("support_tickets", 0, 10, int(row["support_tickets"]))
sim_revenue = st.slider("revenue", 0, 1000, float(row["revenue"]))

if st.button("Recompute Churn"):
    sim_df = row.to_frame().T
    sim_df["num_sessions"] = sim_num_sessions
    sim_df["support_tickets"] = sim_support
    sim_df["revenue"] = sim_revenue
    sim_feat = prepare_features(sim_df)
    sim_pred = run_predictions(sim_feat, model).iloc[0]
    st.success(f"New churn probability: {sim_pred['churn_prob']:.2f}")
    sim_action = actions.recommend_action(sim_feat.iloc[0])
    st.json(sim_action)

st.caption("Churn Intelligence Platform · Streamlit")

