import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY",
        "EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3","DAYS_BIRTH","DAYS_EMPLOYED",
        "CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE","NAME_FAMILY_STATUS","NAME_HOUSING_TYPE"
    ])
    # Derived features
    df["AGE"] = (df["DAYS_BIRTH"].abs()/365).astype(int)
    df["EmploymentYears"] = (df["DAYS_EMPLOYED"].abs()/365).astype(int)
    df["CreditIncomeRatio"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    df["AnnuityIncomeRatio"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
    df["AvgExternalScore"] = df[["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"]].mean(axis=1)
    return df

df = load_data()

st.title("🔎 Page 20 – Customer Risk Explorer")

# Sidebar: Select Customer ID
customer_id = st.sidebar.selectbox("Select Customer ID", df["SK_ID_CURR"].unique())
cust = df[df["SK_ID_CURR"] == customer_id].iloc[0]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Default Status", "Defaulter" if cust["TARGET"]==1 else "Non-Defaulter")
col2.metric("Age", f"{cust['AGE']} years")
col3.metric("Income", f"{cust['AMT_INCOME_TOTAL']:,.0f}")
col4.metric("Credit", f"{cust['AMT_CREDIT']:,.0f}")

col5, col6, col7 = st.columns(3)
col5.metric("Credit/Income Ratio", f"{cust['CreditIncomeRatio']:.2f}")
col6.metric("Annuity/Income Ratio", f"{cust['AnnuityIncomeRatio']:.2f}")
col7.metric("Avg External Score", f"{cust['AvgExternalScore']:.2f}")

# Visualization 1: Credit vs Income Scatter Plot
st.subheader("Credit vs Income (Customer Highlight)")
fig1 = px.scatter(df, x="AMT_INCOME_TOTAL", y="AMT_CREDIT", color="TARGET", opacity=0.4,
                  title="Credit vs Income")
fig1.add_scatter(x=[cust["AMT_INCOME_TOTAL"]], y=[cust["AMT_CREDIT"]],
                 mode="markers", marker=dict(color="red", size=12), name="Selected Customer")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: External Score vs TARGET
st.subheader("External Score vs Default")
fig2 = px.box(df, x="TARGET", y="AvgExternalScore", color="TARGET",
              title="External Score vs TARGET")
fig2.add_scatter(x=[cust["TARGET"]], y=[cust["AvgExternalScore"]],
                 mode="markers", marker=dict(color="red", size=12), name="Selected Customer")
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Income vs Family Size
st.subheader("Income vs Family Size")
fig3 = px.scatter(df, x="NAME_FAMILY_STATUS", y="AMT_INCOME_TOTAL", color="TARGET", opacity=0.5,
                  title="Income vs Family Status")
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Credit vs Housing Type
st.subheader("Credit vs Housing Type")
fig4 = px.box(df, x="NAME_HOUSING_TYPE", y="AMT_CREDIT", color="TARGET",
              title="Credit vs Housing Type")
st.plotly_chart(fig4, use_container_width=True)

# Risk Factor Summary
st.subheader("Risk Factor Summary")
risk_factors = {
    "Low External Score (<0.3)": cust["AvgExternalScore"] < 0.3,
    "High Credit/Income Ratio (>6)": cust["CreditIncomeRatio"] > 6,
    "High Annuity/Income Ratio (>0.3)": cust["AnnuityIncomeRatio"] > 0.3,
    "Young Age (<30)": cust["AGE"] < 30,
    "Short Employment (<2 years)": cust["EmploymentYears"] < 2
}
risk_df = pd.DataFrame(list(risk_factors.items()), columns=["Risk Factor","Flag"])
st.dataframe(risk_df)

# Customer Record
st.subheader("Customer Record")
st.write(cust)
