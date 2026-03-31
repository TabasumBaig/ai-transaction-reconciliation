import streamlit as st
import pandas as pd

st.title("💳 Transaction Reconciliation Dashboard")

df = pd.read_csv("../data/final_report.csv")

st.write("### Full Report")
st.dataframe(df)

# Filter by issue
issue = st.selectbox("Filter by Issue", ["All"] + list(df["issue"].unique()))

if issue != "All":
    filtered = df[df["issue"] == issue]
    st.write(filtered)