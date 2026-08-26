import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","REGION_POPULATION_RELATIVE",
        "REGION_RATING_CLIENT","REGION_RATING_CLIENT_W_CITY",
        "REG_REGION_NOT_LIVE_REGION","REG_REGION_NOT_WORK_REGION",
        "REG_CITY_NOT_LIVE_CITY","REG_CITY_NOT_WORK_CITY",
        "AMT_CREDIT","AMT_INCOME_TOTAL"
    ])
    return df

df = load_data()

st.title("🌍 Regional Risk Analysis")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Most Common Region Rating", df["REGION_RATING_CLIENT"].mode()[0])
col2.metric("Highest Risk Region Rating", df.groupby("REGION_RATING_CLIENT")["TARGET"].mean().idxmax())
col3.metric("Avg Population Indicator", f"{df['REGION_POPULATION_RELATIVE'].mean():.3f}")

# Chart: Customers by Region Rating
st.subheader("Customers by Region Rating")
fig1 = px.histogram(df, x="REGION_RATING_CLIENT", color="TARGET", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# Chart: Default Rate by Region Rating
st.subheader("Default Rate by Region Rating")
region_default = df.groupby("REGION_RATING_CLIENT")["TARGET"].mean().reset_index()
fig2 = px.bar(region_default, x="REGION_RATING_CLIENT", y="TARGET", title="Default Rate (%) by Region Rating")
st.plotly_chart(fig2, use_container_width=True)

# Chart: Credit by Region Rating
st.subheader("Credit by Region Rating")
fig3 = px.box(df, x="REGION_RATING_CLIENT", y="AMT_CREDIT", color="TARGET")
st.plotly_chart(fig3, use_container_width=True)

# Chart: Income by Region Rating
st.subheader("Income by Region Rating")
fig4 = px.box(df, x="REGION_RATING_CLIENT", y="AMT_INCOME_TOTAL", color="TARGET")
st.plotly_chart(fig4, use_container_width=True)

# Chart: Region Mismatch vs Default
st.subheader("Region Mismatch vs Default")
fig5 = px.histogram(df, x="REG_REGION_NOT_LIVE_REGION", color="TARGET", barmode="group", title="Live Region Mismatch")
st.plotly_chart(fig5, use_container_width=True)
fig6 = px.histogram(df, x="REG_REGION_NOT_WORK_REGION", color="TARGET", barmode="group", title="Work Region Mismatch")
st.plotly_chart(fig6, use_container_width=True)

# Chart: City Mismatch vs Default
st.subheader("City Mismatch vs Default")
fig7 = px.histogram(df, x="REG_CITY_NOT_LIVE_CITY", color="TARGET", barmode="group", title="Live City Mismatch")
st.plotly_chart(fig7, use_container_width=True)
fig8 = px.histogram(df, x="REG_CITY_NOT_WORK_CITY", color="TARGET", barmode="group", title="Work City Mismatch")
st.plotly_chart(fig8, use_container_width=True)

# Table
st.subheader("Sample Records")
st.dataframe(df[["SK_ID_CURR","TARGET","REGION_POPULATION_RELATIVE","REGION_RATING_CLIENT",
                 "REGION_RATING_CLIENT_W_CITY","REG_REGION_NOT_LIVE_REGION","REG_REGION_NOT_WORK_REGION",
                 "REG_CITY_NOT_LIVE_CITY","REG_CITY_NOT_WORK_CITY","AMT_CREDIT","AMT_INCOME_TOTAL"]].head(20))
