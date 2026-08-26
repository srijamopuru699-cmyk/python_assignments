import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","NAME_EDUCATION_TYPE","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY"
    ])
    return df

df = load_data()

st.title("🎓 Education Analysis")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Most Common Education", df["NAME_EDUCATION_TYPE"].mode()[0])
col2.metric("Highest Income Group", df.groupby("NAME_EDUCATION_TYPE")["AMT_INCOME_TOTAL"].mean().idxmax())
col3.metric("Lowest Default Group", df.groupby("NAME_EDUCATION_TYPE")["TARGET"].mean().idxmin())
col4.metric("Highest Default Group", df.groupby("NAME_EDUCATION_TYPE")["TARGET"].mean().idxmax())

# Chart: Customers by Education
st.subheader("Customers by Education")
fig1 = px.histogram(df, x="NAME_EDUCATION_TYPE", color="TARGET", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# Chart: Default Rate by Education
st.subheader("Default Rate by Education")
edu_default = df.groupby("NAME_EDUCATION_TYPE")["TARGET"].mean().reset_index()
fig2 = px.bar(edu_default, x="NAME_EDUCATION_TYPE", y="TARGET", title="Default Rate (%) by Education")
st.plotly_chart(fig2, use_container_width=True)

# Chart: Income by Education
st.subheader("Income by Education")
fig3 = px.box(df, x="NAME_EDUCATION_TYPE", y="AMT_INCOME_TOTAL", color="TARGET")
st.plotly_chart(fig3, use_container_width=True)

# Chart: Credit by Education
st.subheader("Credit by Education")
fig4 = px.box(df, x="NAME_EDUCATION_TYPE", y="AMT_CREDIT", color="TARGET")
st.plotly_chart(fig4, use_container_width=True)

# Chart: Annuity by Education
st.subheader("Annuity by Education")
fig5 = px.box(df, x="NAME_EDUCATION_TYPE", y="AMT_ANNUITY", color="TARGET")
st.plotly_chart(fig5, use_container_width=True)

# Chart: Credit-to-Income Ratio by Education
st.subheader("Credit-to-Income Ratio by Education")
df["CreditIncomeRatio"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
fig6 = px.box(df, x="NAME_EDUCATION_TYPE", y="CreditIncomeRatio", color="TARGET")
st.plotly_chart(fig6, use_container_width=True)

# Table
st.subheader("Sample Records")
st.dataframe(df[["SK_ID_CURR","TARGET","NAME_EDUCATION_TYPE","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY"]].head(20))
