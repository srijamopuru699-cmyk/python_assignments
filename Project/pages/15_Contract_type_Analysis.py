import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","NAME_CONTRACT_TYPE","AMT_CREDIT","AMT_INCOME_TOTAL","AMT_ANNUITY"
    ])
    return df

df = load_data()

st.title("📑 Contract Type Analysis")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Cash Loan Applications", (df["NAME_CONTRACT_TYPE"]=="Cash loans").sum())
col2.metric("Revolving Loan Applications", (df["NAME_CONTRACT_TYPE"]=="Revolving loans").sum())
col3.metric("Cash Loan Default Rate", f"{df.loc[df['NAME_CONTRACT_TYPE']=='Cash loans','TARGET'].mean()*100:.2f}%")
col4.metric("Revolving Loan Default Rate", f"{df.loc[df['NAME_CONTRACT_TYPE']=='Revolving loans','TARGET'].mean()*100:.2f}%")

# Chart: Applications by Contract Type
st.subheader("Applications by Contract Type")
fig1 = px.histogram(df, x="NAME_CONTRACT_TYPE", color="TARGET", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# Chart: Default Rate by Contract Type
st.subheader("Default Rate by Contract Type")
contract_default = df.groupby("NAME_CONTRACT_TYPE")["TARGET"].mean().reset_index()
fig2 = px.bar(contract_default, x="NAME_CONTRACT_TYPE", y="TARGET", title="Default Rate (%) by Contract Type")
st.plotly_chart(fig2, use_container_width=True)

# Chart: Average Credit by Contract Type
st.subheader("Average Credit by Contract Type")
credit_avg = df.groupby("NAME_CONTRACT_TYPE")["AMT_CREDIT"].mean().reset_index()
fig3 = px.bar(credit_avg, x="NAME_CONTRACT_TYPE", y="AMT_CREDIT", title="Average Credit by Contract Type")
st.plotly_chart(fig3, use_container_width=True)

# Chart: Average Income by Contract Type
st.subheader("Average Income by Contract Type")
income_avg = df.groupby("NAME_CONTRACT_TYPE")["AMT_INCOME_TOTAL"].mean().reset_index()
fig4 = px.bar(income_avg, x="NAME_CONTRACT_TYPE", y="AMT_INCOME_TOTAL", title="Average Income by Contract Type")
st.plotly_chart(fig4, use_container_width=True)

# Chart: Average Annuity by Contract Type
st.subheader("Average Annuity by Contract Type")
annuity_avg = df.groupby("NAME_CONTRACT_TYPE")["AMT_ANNUITY"].mean().reset_index()
fig5 = px.bar(annuity_avg, x="NAME_CONTRACT_TYPE", y="AMT_ANNUITY", title="Average Annuity by Contract Type")
st.plotly_chart(fig5, use_container_width=True)

# Chart: Credit-to-Income Ratio by Contract Type
st.subheader("Credit-to-Income Ratio by Contract Type")
df["CreditIncomeRatio"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
fig6 = px.box(df, x="NAME_CONTRACT_TYPE", y="CreditIncomeRatio", color="TARGET")
st.plotly_chart(fig6, use_container_width=True)

# Table
st.subheader("Sample Records")
st.dataframe(df[["SK_ID_CURR","TARGET","NAME_CONTRACT_TYPE","AMT_CREDIT","AMT_INCOME_TOTAL","AMT_ANNUITY"]].head(20))
