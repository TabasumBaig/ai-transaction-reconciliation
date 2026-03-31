import streamlit as st
import pandas as pd
import os

st.title("💳 Transaction Reconciliation Dashboard")

# Debug: show current files
st.write("📂 Files in project:")
st.write(os.listdir())

# Try loading file
try:
    df = pd.read_csv("data/final_report.csv")
    
    st.success("✅ Data loaded successfully")

    st.write("### Full Report")
    st.dataframe(df)

    issue = st.selectbox("Filter by Issue", ["All"] + list(df["issue"].dropna().unique()))

    if issue != "All":
        st.write(df[df["issue"] == issue])

except Exception as e:
    st.error("❌ Error loading file")
    st.write(str(e))