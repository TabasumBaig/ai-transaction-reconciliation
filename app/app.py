import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Reconciliation Dashboard", layout="wide")

st.title("💳 Transaction Reconciliation Dashboard")

# -------------------------------
# Load data (works locally + deployment)
# -------------------------------
file_path = "data/final_report.csv"

if not os.path.exists(file_path):
    st.error("❌ Data file not found. Please check path.")
else:
    df = pd.read_csv(file_path)

    # -------------------------------
    # Show full data
    # -------------------------------
    st.write("### 📊 Full Report")
    st.dataframe(df, use_container_width=True)

    # -------------------------------
    # Filter section
    # -------------------------------
    st.write("### 🔍 Filter by Issue")

    issues = ["All"] + sorted(df["issue"].dropna().unique().tolist())
    selected_issue = st.selectbox("Select Issue Type", issues)

    if selected_issue != "All":
        filtered = df[df["issue"] == selected_issue]
        st.write(f"### Showing: {selected_issue}")
        st.dataframe(filtered, use_container_width=True)

    # -------------------------------
    # Summary
    # -------------------------------
    st.write("### 📈 Issue Summary")
    summary = df["issue"].value_counts().reset_index()
    summary.columns = ["Issue Type", "Count"]
    st.dataframe(summary, use_container_width=True)