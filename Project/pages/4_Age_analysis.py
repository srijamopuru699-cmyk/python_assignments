import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/application_train.csv", usecols=[
    "SK_ID_CURR","TARGET","DAYS_BIRTH","AMT_CREDIT","AMT_INCOME_TOTAL"
])
df["AGE"] = (df["DAYS_BIRTH"].abs() / 365).astype(int)

# Define Age Groups
bins = [18,25,30,35,40,45,50,55,60,100]
labels = ["18-25","26-30","31-35","36-40","41-45","46-50","51-55","56-60","61+"]
df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins, labels=labels, right=True)

# Page Title
st.title("📊 Age Analysis")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Age", f"{df['AGE'].mean():.1f}")
col2.metric("Youngest Customer", df['AGE'].min())
col3.metric("Oldest Customer", df['AGE'].max())
risk_group = df.groupby("AGE_GROUP")["TARGET"].mean().idxmax()
col4.metric("Highest Risk Age Group", risk_group)

# Age Distribution Histogram
st.subheader("Age Distribution")
st.plotly_chart(px.histogram(df, x="AGE", nbins=40, color="TARGET"), use_container_width=True)

# Applications by Age Group
st.subheader("Applications by Age Group")
st.plotly_chart(px.histogram(df, x="AGE_GROUP", color="TARGET", barmode="group"), use_container_width=True)

# Default Rate by Age
st.subheader("Default Rate by Age")
age_rate = df.groupby("AGE")["TARGET"].mean().reset_index()
st.plotly_chart(px.line(age_rate, x="AGE", y="TARGET", title="Default Rate by Age"), use_container_width=True)

# Default Rate by Age Group
st.subheader("Default Rate by Age Group")
group_rate = df.groupby("AGE_GROUP")["TARGET"].mean().reset_index()
st.plotly_chart(px.bar(group_rate, x="AGE_GROUP", y="TARGET", title="Default Rate by Age Group"), use_container_width=True)

# Credit Amount by Age
st.subheader("Credit Amount by Age")
st.plotly_chart(px.scatter(df, x="AGE", y="AMT_CREDIT", color="TARGET", title="Credit Amount by Age"), use_container_width=True)

# Income by Age
st.subheader("Income by Age")
st.plotly_chart(px.scatter(df, x="AGE", y="AMT_INCOME_TOTAL", color="TARGET", title="Income by Age"), use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","AGE","AGE_GROUP","AMT_CREDIT","AMT_INCOME_TOTAL"]].head(20))
