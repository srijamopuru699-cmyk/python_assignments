import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/application_train.csv", usecols=[
    "SK_ID_CURR","TARGET","CODE_GENDER","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY"
])

# Page Title
st.title("👩‍🦰🧑 Gender Analysis")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Male Applicants", (df["CODE_GENDER"]=="M").sum())
col2.metric("Female Applicants", (df["CODE_GENDER"]=="F").sum())
col3.metric("Male Default Rate %", f"{df.loc[df['CODE_GENDER']=='M','TARGET'].mean()*100:.2f}")
col4.metric("Female Default Rate %", f"{df.loc[df['CODE_GENDER']=='F','TARGET'].mean()*100:.2f}")

# Applicants by Gender
st.subheader("Applicants by Gender")
st.plotly_chart(px.histogram(df, x="CODE_GENDER", color="TARGET", barmode="group"), use_container_width=True)

# Default Customers by Gender
st.subheader("Default Customers by Gender")
gender_defaults = df.groupby("CODE_GENDER")["TARGET"].sum().reset_index()
st.plotly_chart(px.bar(gender_defaults, x="CODE_GENDER", y="TARGET", title="Defaults by Gender"), use_container_width=True)

# Default Rate by Gender
st.subheader("Default Rate by Gender")
gender_rate = df.groupby("CODE_GENDER")["TARGET"].mean().reset_index()
st.plotly_chart(px.bar(gender_rate, x="CODE_GENDER", y="TARGET", title="Default Rate by Gender"), use_container_width=True)

# Average Income by Gender
st.subheader("Average Income by Gender")
income_gender = df.groupby("CODE_GENDER")["AMT_INCOME_TOTAL"].mean().reset_index()
st.plotly_chart(px.bar(income_gender, x="CODE_GENDER", y="AMT_INCOME_TOTAL", title="Avg Income by Gender"), use_container_width=True)

# Average Credit by Gender
st.subheader("Average Credit by Gender")
credit_gender = df.groupby("CODE_GENDER")["AMT_CREDIT"].mean().reset_index()
st.plotly_chart(px.bar(credit_gender, x="CODE_GENDER", y="AMT_CREDIT", title="Avg Credit by Gender"), use_container_width=True)

# Average Annuity by Gender
st.subheader("Average Annuity by Gender")
annuity_gender = df.groupby("CODE_GENDER")["AMT_ANNUITY"].mean().reset_index()
st.plotly_chart(px.bar(annuity_gender, x="CODE_GENDER", y="AMT_ANNUITY", title="Avg Annuity by Gender"), use_container_width=True)

# Comparison Table
st.subheader("Comparison Table")
comparison = df.groupby("CODE_GENDER").agg(
    Customers=("SK_ID_CURR","count"),
    Defaults=("TARGET","sum"),
    Default_Rate=("TARGET","mean"),
    Avg_Income=("AMT_INCOME_TOTAL","mean"),
    Avg_Credit=("AMT_CREDIT","mean"),
    Avg_Annuity=("AMT_ANNUITY","mean")
).reset_index()
st.dataframe(comparison)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","CODE_GENDER","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY"]].head(20))
