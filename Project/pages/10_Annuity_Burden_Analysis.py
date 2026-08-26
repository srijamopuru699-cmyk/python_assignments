import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","AMT_ANNUITY","AMT_INCOME_TOTAL",
        "CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE"
    ])
    df["AnnuityIncomeRatio"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
    return df

df = load_data()

st.title("📊 Page 10 – Annuity Burden Analysis")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Annuity", f"{df['AMT_ANNUITY'].mean():,.0f}")
col2.metric("Median Annuity", f"{df['AMT_ANNUITY'].median():,.0f}")
col3.metric("Average Annuity/Income Ratio", f"{df['AnnuityIncomeRatio'].mean():.3f}")
col4.metric("High Burden % (>0.3)", f"{(df['AnnuityIncomeRatio']>0.3).mean()*100:.2f}%")

# Visualization 1: Annuity-to-Income Distribution
st.subheader("Annuity-to-Income Ratio Distribution")
fig1 = px.histogram(df, x="AnnuityIncomeRatio", nbins=40, color="TARGET",
                    title="Distribution of Annuity Burden by Default Status")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Default Rate by Ratio
st.subheader("Default Rate by Annuity-to-Income Ratio")
df["RatioBin"] = pd.cut(df["AnnuityIncomeRatio"], bins=10)
df["RatioBin"] = df["RatioBin"].astype(str)  # convert Interval to string
ratio_default = df.groupby("RatioBin")["TARGET"].mean().reset_index()
fig2 = px.bar(ratio_default, x="RatioBin", y="TARGET", title="Default Rate by Ratio")
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Ratio by Gender
st.subheader("Annuity Burden by Gender")
fig3 = px.box(df, x="CODE_GENDER", y="AnnuityIncomeRatio", color="TARGET",
              title="Annuity Burden by Gender")
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Ratio by Income Type
st.subheader("Annuity Burden by Income Type")
fig4 = px.box(df, x="NAME_INCOME_TYPE", y="AnnuityIncomeRatio", color="TARGET",
              title="Annuity Burden by Income Type")
st.plotly_chart(fig4, use_container_width=True)

# Visualization 5: Ratio by Education
st.subheader("Annuity Burden by Education")
fig5 = px.box(df, x="NAME_EDUCATION_TYPE", y="AnnuityIncomeRatio", color="TARGET",
              title="Annuity Burden by Education")
st.plotly_chart(fig5, use_container_width=True)

# Visualization 6: Ratio vs TARGET
st.subheader("Annuity-to-Income Ratio vs Default Status")
fig6 = px.box(df, x="TARGET", y="AnnuityIncomeRatio", color="TARGET",
              title="Annuity-to-Income Ratio vs TARGET")
st.plotly_chart(fig6, use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","AMT_INCOME_TOTAL","AMT_ANNUITY","AnnuityIncomeRatio","CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE"]].head(20))
