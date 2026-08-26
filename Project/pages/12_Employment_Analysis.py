import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","DAYS_EMPLOYED","NAME_INCOME_TYPE",
        "OCCUPATION_TYPE","ORGANIZATION_TYPE"
    ])
    # Clean special values (365243 means missing)
    df = df[df["DAYS_EMPLOYED"] < 0]
    df["EmploymentYears"] = (df["DAYS_EMPLOYED"].abs()/365).astype(int)
    return df

df = load_data()

st.title("👔 Page 12 – Employment Analysis")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Employment Years", f"{df['EmploymentYears'].mean():.1f}")
col2.metric("Most Common Occupation", df["OCCUPATION_TYPE"].mode()[0] if not df["OCCUPATION_TYPE"].isnull().all() else "Unknown")
col3.metric("Most Common Income Type", df["NAME_INCOME_TYPE"].mode()[0])
# Highest Risk Occupation (based on default rate)
occ_default = df.groupby("OCCUPATION_TYPE")["TARGET"].mean().reset_index().dropna()
highest_risk_occ = occ_default.loc[occ_default["TARGET"].idxmax(),"OCCUPATION_TYPE"]
col4.metric("Highest Risk Occupation", highest_risk_occ)

# Visualization 1: Employment Years Distribution
st.subheader("Employment Years Distribution")
fig1 = px.histogram(df, x="EmploymentYears", nbins=40, color="TARGET",
                    title="Distribution of Employment Years by Default Status")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Default Rate by Employment Years
st.subheader("Default Rate by Employment Years")
emp_default = df.groupby("EmploymentYears")["TARGET"].mean().reset_index()
fig2 = px.line(emp_default, x="EmploymentYears", y="TARGET", title="Default Rate by Employment Years")
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Applications by Income Type
st.subheader("Applications by Income Type")
fig3 = px.histogram(df, x="NAME_INCOME_TYPE", color="TARGET", barmode="group",
                    title="Applications by Income Type")
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Default Rate by Income Type
st.subheader("Default Rate by Income Type")
income_default = df.groupby("NAME_INCOME_TYPE")["TARGET"].mean().reset_index()
fig4 = px.bar(income_default, x="NAME_INCOME_TYPE", y="TARGET", title="Default Rate by Income Type")
st.plotly_chart(fig4, use_container_width=True)

# Visualization 5: Applications by Occupation
st.subheader("Applications by Occupation")
fig5 = px.histogram(df, x="OCCUPATION_TYPE", color="TARGET",
                    title="Applications by Occupation")
st.plotly_chart(fig5, use_container_width=True)

# Visualization 6: Default Rate by Occupation
st.subheader("Default Rate by Occupation")
fig6 = px.bar(occ_default, x="OCCUPATION_TYPE", y="TARGET", title="Default Rate by Occupation")
st.plotly_chart(fig6, use_container_width=True)

# Visualization 7: Default Rate by Organization Type
st.subheader("Default Rate by Organization Type")
org_default = df.groupby("ORGANIZATION_TYPE")["TARGET"].mean().reset_index().dropna()
fig7 = px.bar(org_default, x="ORGANIZATION_TYPE", y="TARGET", title="Default Rate by Organization Type")
st.plotly_chart(fig7, use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","EmploymentYears","NAME_INCOME_TYPE","OCCUPATION_TYPE","ORGANIZATION_TYPE"]].head(20))
