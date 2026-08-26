import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/application_train.csv", usecols=[
    "SK_ID_CURR","TARGET","CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE","NAME_CONTRACT_TYPE","AMT_CREDIT"
])

# Page Title
st.title("💳 Credit Analysis")

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Credit", f"{df['AMT_CREDIT'].sum():,.0f}")
col2.metric("Average Credit", f"{df['AMT_CREDIT'].mean():,.0f}")
col3.metric("Median Credit", f"{df['AMT_CREDIT'].median():,.0f}")
col4.metric("Maximum Credit", f"{df['AMT_CREDIT'].max():,.0f}")
col5.metric("Minimum Credit", f"{df['AMT_CREDIT'].min():,.0f}")

# Credit Amount Distribution
st.subheader("Credit Amount Distribution")
st.plotly_chart(px.histogram(df, x="AMT_CREDIT", nbins=40, color="TARGET"), use_container_width=True)

# Credit Amount by TARGET
st.subheader("Credit Amount by Default Status")
target_credit = df.groupby("TARGET")["AMT_CREDIT"].mean().reset_index()
st.plotly_chart(px.bar(target_credit, x="TARGET", y="AMT_CREDIT", title="Avg Credit by Default Status"), use_container_width=True)

# Average Credit by Gender
st.subheader("Average Credit by Gender")
gender_credit = df.groupby("CODE_GENDER")["AMT_CREDIT"].mean().reset_index()
st.plotly_chart(px.bar(gender_credit, x="CODE_GENDER", y="AMT_CREDIT", title="Avg Credit by Gender"), use_container_width=True)

# Credit by Income Type
st.subheader("Average Credit by Income Type")
income_credit = df.groupby("NAME_INCOME_TYPE")["AMT_CREDIT"].mean().reset_index()
st.plotly_chart(px.bar(income_credit, x="NAME_INCOME_TYPE", y="AMT_CREDIT", title="Avg Credit by Income Type"), use_container_width=True)

# Credit by Education
st.subheader("Average Credit by Education")
edu_credit = df.groupby("NAME_EDUCATION_TYPE")["AMT_CREDIT"].mean().reset_index()
st.plotly_chart(px.bar(edu_credit, x="NAME_EDUCATION_TYPE", y="AMT_CREDIT", title="Avg Credit by Education"), use_container_width=True)

# Credit by Contract Type
st.subheader("Average Credit by Contract Type")
contract_credit = df.groupby("NAME_CONTRACT_TYPE")["AMT_CREDIT"].mean().reset_index()
st.plotly_chart(px.bar(contract_credit, x="NAME_CONTRACT_TYPE", y="AMT_CREDIT", title="Avg Credit by Contract Type"), use_container_width=True)

# Default Rate by Credit Range
st.subheader("Default Rate by Credit Range")
df["Credit_Range"] = pd.cut(df["AMT_CREDIT"],
                            bins=[0,50000,100000,200000,500000,1000000,2000000,5000000],
                            labels=["<50K","50K–100K","100K–200K","200K–500K","500K–1M","1M–2M","Above 2M"])
credit_rate = df.groupby("Credit_Range")["TARGET"].mean().reset_index()
st.plotly_chart(px.bar(credit_rate, x="Credit_Range", y="TARGET", title="Default Rate by Credit Range"), use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE","NAME_CONTRACT_TYPE","AMT_CREDIT","Credit_Range"]].head(20))
