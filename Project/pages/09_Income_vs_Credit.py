import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","CODE_GENDER","NAME_EDUCATION_TYPE"
    ])
    df["CreditIncomeRatio"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    return df

df = load_data()

st.title("💰 Income vs Credit Analysis")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Avg Credit/Income Ratio", f"{df['CreditIncomeRatio'].mean():.2f}")
col2.metric("Highest Ratio", f"{df['CreditIncomeRatio'].max():.2f}")
col3.metric("High-Risk Ratio %", f"{(df['CreditIncomeRatio']>6).mean()*100:.2f}")

# Risk Groups
def risk_group(r):
    if r < 2: return "Low"
    elif r < 4: return "Moderate"
    elif r < 6: return "High"
    else: return "Very High"

df["RiskGroup"] = df["CreditIncomeRatio"].apply(risk_group)

# Chart: Income vs Credit Scatter
st.subheader("Income vs Credit")
fig1 = px.scatter(df, x="AMT_INCOME_TOTAL", y="AMT_CREDIT", color="TARGET", opacity=0.5)
st.plotly_chart(fig1, use_container_width=True)

# Chart: Credit-to-Income Ratio Distribution
st.subheader("Credit-to-Income Ratio Distribution")
fig2 = px.histogram(df, x="CreditIncomeRatio", nbins=40, color="TARGET")
st.plotly_chart(fig2, use_container_width=True)

# Chart: Default Rate by Risk Group
st.subheader("Default Rate by Risk Group")
risk_default = df.groupby("RiskGroup")["TARGET"].mean().reset_index()
fig3 = px.bar(risk_default, x="RiskGroup", y="TARGET", title="Default Rate (%) by Risk Group")
st.plotly_chart(fig3, use_container_width=True)

# Chart: Gender-wise Credit/Income Ratio
st.subheader("Gender-wise Credit/Income Ratio")
fig4 = px.box(df, x="CODE_GENDER", y="CreditIncomeRatio", color="TARGET")
st.plotly_chart(fig4, use_container_width=True)

# Chart: Education-wise Credit/Income Ratio
st.subheader("Education-wise Credit/Income Ratio")
fig5 = px.box(df, x="NAME_EDUCATION_TYPE", y="CreditIncomeRatio", color="TARGET")
st.plotly_chart(fig5, use_container_width=True)

# Table
st.subheader("Sample Records")
st.dataframe(df[["SK_ID_CURR","TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","CreditIncomeRatio","RiskGroup"]].head(20))
