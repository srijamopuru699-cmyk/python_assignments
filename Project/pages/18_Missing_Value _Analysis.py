import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/application_train.csv")

# Page Title
st.title("❓ Missing Values Analysis")

# Calculate missing values
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
missing_df = pd.DataFrame({
    "Column": missing.index,
    "MissingCount": missing.values,
    "MissingPct": (missing.values / len(df)) * 100,
    "DataType": [str(df[col].dtype) for col in missing.index]   # ✅ force dtype to string
})

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Rows", len(df))
col2.metric("Total Columns", df.shape[1])
col3.metric("Total Missing Values", int(missing.sum()))
col4.metric("Columns with Missing", len(missing_df))
col5.metric(">50% Missing Columns", (missing_df["MissingPct"] > 50).sum())

# Top 20 Columns with Missing Values
st.subheader("Top 20 Columns with Missing Values")
fig1 = px.bar(missing_df.head(20), x="Column", y="MissingPct", title="Missing Percentage by Column")
st.plotly_chart(fig1, use_container_width=True)

# Overall Missing Percentage by Column
st.subheader("Missing Percentage by Column")
fig2 = px.bar(missing_df, x="Column", y="MissingPct", title="Overall Missing Percentage")
st.plotly_chart(fig2, use_container_width=True)

# Missing Values by Data Type
st.subheader("Missing Values by Data Type")
dtype_missing = missing_df.groupby("DataType", as_index=False)["MissingCount"].sum()
fig3 = px.bar(dtype_missing, x="DataType", y="MissingCount", title="Missing Values by Data Type")
st.plotly_chart(fig3, use_container_width=True)

# Heatmap of Missing Values by Row (sample)
st.subheader("Heatmap of Missing Values by Row (first 200 rows)")
sample_df = df.head(200)  # limit rows for visualization
plt.figure(figsize=(12,6))
sns.heatmap(sample_df.isnull(), cbar=False)
st.pyplot(plt)

# Table
st.subheader("Missing Value Summary")
st.dataframe(missing_df.head(20))
