import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","AMT_CREDIT","AMT_INCOME_TOTAL","AMT_ANNUITY"
    ])
    return df

df = load_data()

st.title("🏦 Executive Overview")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Applications", len(df))
col2.metric("Total Default Customers", (df["TARGET"]==1).sum())
col3.metric("Total Non-Default Customers", (df["TARGET"]==0).sum())
col4.metric("Default Rate %", f"{df['TARGET'].mean()*100:.2f}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Total Credit Amount", f"{df['AMT_CREDIT'].sum():,.0f}")
col6.metric("Average Credit Amount", f"{df['AMT_CREDIT'].mean():,.0f}")
col7.metric("Average Income", f"{df['AMT_INCOME_TOTAL'].mean():,.0f}")
col8.metric("Average Annuity", f"{df['AMT_ANNUITY'].mean():,.0f}")

# Chart: Default vs Non-Default
st.subheader("Default vs Non-Default Customers")
fig1 = px.histogram(df, x="TARGET", color="TARGET", labels={"TARGET":"Default Status"})
st.plotly_chart(fig1, use_container_width=True)

# Chart: Credit Amount Distribution
st.subheader("Credit Amount Distribution")
fig2 = px.histogram(df, x="AMT_CREDIT", nbins=40, color="TARGET")
st.plotly_chart(fig2, use_container_width=True)

# Chart: Income Distribution
st.subheader("Income Distribution")
fig3 = px.histogram(df, x="AMT_INCOME_TOTAL", nbins=40, color="TARGET")
st.plotly_chart(fig3, use_container_width=True)

# Chart: Annuity Distribution
st.subheader("Annuity Distribution")
fig4 = px.histogram(df, x="AMT_ANNUITY", nbins=40, color="TARGET")
st.plotly_chart(fig4, use_container_width=True)

# Table
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","AMT_CREDIT","AMT_INCOME_TOTAL","AMT_ANNUITY"]].head(20))