import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/application_train.csv", usecols=[
    "SK_ID_CURR","TARGET","AMT_ANNUITY","AMT_INCOME_TOTAL","AMT_CREDIT","NAME_INCOME_TYPE"
])

# Page Title
st.title("📑 Page 9 – Annuity Analysis")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Annuity", f"{df['AMT_ANNUITY'].mean():,.0f}")
col2.metric("Median Annuity", f"{df['AMT_ANNUITY'].median():,.0f}")
col3.metric("Maximum Annuity", f"{df['AMT_ANNUITY'].max():,.0f}")
col4.metric("Avg Annuity (Defaulters)", f"{df.loc[df['TARGET']==1,'AMT_ANNUITY'].mean():,.0f}")

# Annuity Distribution
st.subheader("Annuity Distribution")
st.plotly_chart(px.histogram(df, x="AMT_ANNUITY", nbins=40, color="TARGET"), use_container_width=True)

# Annuity by TARGET
st.subheader("Annuity by Default Status")
st.plotly_chart(px.box(df, x="TARGET", y="AMT_ANNUITY", color="TARGET"), use_container_width=True)

# Annuity vs Income
st.subheader("Annuity vs Income")
st.plotly_chart(px.scatter(df, x="AMT_INCOME_TOTAL", y="AMT_ANNUITY", color="TARGET", opacity=0.5), use_container_width=True)

# Annuity vs Credit
st.subheader("Annuity vs Credit")
st.plotly_chart(px.scatter(df, x="AMT_CREDIT", y="AMT_ANNUITY", color="TARGET", opacity=0.5), use_container_width=True)

# Average Annuity by Income Type
st.subheader("Average Annuity by Income Type")
income_annuity = df.groupby("NAME_INCOME_TYPE")["AMT_ANNUITY"].mean().reset_index()
st.plotly_chart(px.bar(income_annuity, x="NAME_INCOME_TYPE", y="AMT_ANNUITY", title="Avg Annuity by Income Type"), use_container_width=True)

# Default Rate by Annuity Group
st.subheader("Default Rate by Annuity Group")
df["Annuity_Group"] = pd.cut(df["AMT_ANNUITY"],
                             bins=[0,5000,10000,20000,30000,50000,100000,200000],
                             labels=["<5K","5K–10K","10K–20K","20K–30K","30K–50K","50K–100K","Above 100K"])
annuity_rate = df.groupby("Annuity_Group")["TARGET"].mean().reset_index()
st.plotly_chart(px.bar(annuity_rate, x="Annuity_Group", y="TARGET", title="Default Rate by Annuity Group"), use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY","NAME_INCOME_TYPE","Annuity_Group"]].head(20))
