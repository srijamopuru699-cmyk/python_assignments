import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","CODE_GENDER","DAYS_BIRTH",
        "NAME_FAMILY_STATUS","NAME_EDUCATION_TYPE",
        "NAME_HOUSING_TYPE","CNT_FAM_MEMBERS"
    ])
    df["AGE"] = (df["DAYS_BIRTH"].abs() / 365).astype(int)
    return df

df = load_data()

# Page Title
st.title("👨‍👩‍👧 Customer Demographic Analysis")

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", len(df))
col2.metric("Average Age", f"{df['AGE'].mean():.1f}")
col3.metric("Male Customers", (df["CODE_GENDER"]=="M").sum())
col4.metric("Female Customers", (df["CODE_GENDER"]=="F").sum())
col5.metric("Avg Family Size", f"{df['CNT_FAM_MEMBERS'].mean():.1f}")

# Customers by Gender
st.subheader("Customers by Gender")
fig1 = px.histogram(df, x="CODE_GENDER", color="TARGET", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# Customers by Age Group
st.subheader("Customers by Age Group")
fig2 = px.histogram(df, x="AGE", color="TARGET", nbins=30)
st.plotly_chart(fig2, use_container_width=True)

# Customers by Family Status
st.subheader("Customers by Family Status")
fig3 = px.histogram(df, x="NAME_FAMILY_STATUS", color="TARGET", barmode="group")
st.plotly_chart(fig3, use_container_width=True)

# Customers by Education
st.subheader("Customers by Education")
fig4 = px.histogram(df, x="NAME_EDUCATION_TYPE", color="TARGET", barmode="group")
st.plotly_chart(fig4, use_container_width=True)

# Customers by Housing Type
st.subheader("Customers by Housing Type")
fig5 = px.histogram(df, x="NAME_HOUSING_TYPE", color="TARGET", barmode="group")
st.plotly_chart(fig5, use_container_width=True)

# Default Rate by Demographic Group
st.subheader("Default Rate by Demographic Group")
demo_cols = ["CODE_GENDER","NAME_FAMILY_STATUS","NAME_EDUCATION_TYPE","NAME_HOUSING_TYPE"]
for col in demo_cols:
    rate = df.groupby(col)["TARGET"].mean().reset_index()
    fig = px.bar(rate, x=col, y="TARGET", title=f"Default Rate by {col}")
    st.plotly_chart(fig, use_container_width=True)

# Sample Records
st.subheader("Sample Records")
st.dataframe(df[["SK_ID_CURR","TARGET","AGE","CODE_GENDER",
                 "NAME_FAMILY_STATUS","NAME_EDUCATION_TYPE",
                 "NAME_HOUSING_TYPE","CNT_FAM_MEMBERS"]].head(20))
