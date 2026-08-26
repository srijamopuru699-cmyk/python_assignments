import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE","NAME_CONTRACT_TYPE"
    ])
    return df

df = load_data()

st.title("🎯 Target / Default Analysis")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Non-Default Customers", (df["TARGET"]==0).sum())
col2.metric("Default Customers", (df["TARGET"]==1).sum())
col3.metric("Default Rate %", f"{df['TARGET'].mean()*100:.2f}")
col4.metric("Non-Default Rate %", f"{(1-df['TARGET'].mean())*100:.2f}")

# Chart: TARGET Count
st.subheader("Default vs Non-Default Count")
fig1 = px.histogram(df, x="TARGET", color="TARGET", labels={"TARGET":"Default Status"})
st.plotly_chart(fig1, use_container_width=True)

# Chart: TARGET Percentage
st.subheader("Default vs Non-Default Percentage")
fig2 = px.pie(df, names="TARGET", title="Default Rate Distribution")
st.plotly_chart(fig2, use_container_width=True)

# Chart: Default Rate by Gender
st.subheader("Default Rate by Gender")
fig3 = px.histogram(df, x="CODE_GENDER", color="TARGET", barmode="group")
st.plotly_chart(fig3, use_container_width=True)

# Chart: Default Rate by Income Type
st.subheader("Default Rate by Income Type")
fig4 = px.histogram(df, x="NAME_INCOME_TYPE", color="TARGET", barmode="group")
st.plotly_chart(fig4, use_container_width=True)

# Chart: Default Rate by Education
st.subheader("Default Rate by Education")
fig5 = px.histogram(df, x="NAME_EDUCATION_TYPE", color="TARGET", barmode="group")
st.plotly_chart(fig5, use_container_width=True)

# Chart: Default Rate by Contract Type
st.subheader("Default Rate by Contract Type")
fig6 = px.histogram(df, x="NAME_CONTRACT_TYPE", color="TARGET", barmode="group")
st.plotly_chart(fig6, use_container_width=True)

# Table
st.subheader("Sample Records")
st.dataframe(df.head(20))

