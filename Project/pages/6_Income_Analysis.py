import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/application_train.csv", usecols=[
    "SK_ID_CURR","TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY"
])

# Page Title
st.title("💵 Income Analysis")

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Income", f"{df['AMT_INCOME_TOTAL'].sum():,.0f}")
col2.metric("Average Income", f"{df['AMT_INCOME_TOTAL'].mean():,.0f}")
col3.metric("Median Income", f"{df['AMT_INCOME_TOTAL'].median():,.0f}")
col4.metric("Maximum Income", f"{df['AMT_INCOME_TOTAL'].max():,.0f}")
col5.metric("Avg Income of Defaulters", f"{df.loc[df['TARGET']==1,'AMT_INCOME_TOTAL'].mean():,.0f}")

# Income Distribution
st.subheader("Income Distribution by Default Status")
st.plotly_chart(px.histogram(df, x="AMT_INCOME_TOTAL", nbins=40, color="TARGET"), use_container_width=True)

# Default Rate by Income Group
st.subheader("Default Rate by Income Group")
df["Income_Group"] = pd.cut(df["AMT_INCOME_TOTAL"],
                            bins=[0,50000,100000,150000,200000,300000,500000,1000000,2000000],
                            labels=["<50K","50K–100K","100K–150K","150K–200K","200K–300K","300K–500K","500K–1M","Above 1M"])
income_rate = df.groupby("Income_Group")["TARGET"].mean().reset_index()
st.plotly_chart(px.bar(income_rate, x="Income_Group", y="TARGET", title="Default Rate by Income Group"), use_container_width=True)

# Credit vs Income
st.subheader("Credit Amount vs Income")
st.plotly_chart(px.scatter(df, x="AMT_INCOME_TOTAL", y="AMT_CREDIT", color="TARGET",
                           title="Credit vs Income"), use_container_width=True)

# Annuity vs Income
st.subheader("Annuity vs Income")
st.plotly_chart(px.scatter(df, x="AMT_INCOME_TOTAL", y="AMT_ANNUITY", color="TARGET",
                           title="Annuity vs Income"), use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY","Income_Group"]].head(20))
