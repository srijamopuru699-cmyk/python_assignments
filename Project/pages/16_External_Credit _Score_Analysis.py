import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/application_train.csv", usecols=[
    "SK_ID_CURR","TARGET","EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"
])

# Page Title
st.title("📊 External Credit Score Analysis")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average EXT_SOURCE_1", f"{df['EXT_SOURCE_1'].mean():.2f}")
col2.metric("Average EXT_SOURCE_2", f"{df['EXT_SOURCE_2'].mean():.2f}")
col3.metric("Average EXT_SOURCE_3", f"{df['EXT_SOURCE_3'].mean():.2f}")
col4.metric("Missing External Score Records", df[["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"]].isnull().sum().sum())

# EXT_SOURCE_1 Distribution
st.subheader("EXT_SOURCE_1 Distribution")
fig1 = px.histogram(df, x="EXT_SOURCE_1", nbins=40, color="TARGET", title="EXT_SOURCE_1 Distribution by Default Status")
st.plotly_chart(fig1, use_container_width=True)

# EXT_SOURCE_2 Distribution
st.subheader("EXT_SOURCE_2 Distribution")
fig2 = px.histogram(df, x="EXT_SOURCE_2", nbins=40, color="TARGET", title="EXT_SOURCE_2 Distribution by Default Status")
st.plotly_chart(fig2, use_container_width=True)

# EXT_SOURCE_3 Distribution
st.subheader("EXT_SOURCE_3 Distribution")
fig3 = px.histogram(df, x="EXT_SOURCE_3", nbins=40, color="TARGET", title="EXT_SOURCE_3 Distribution by Default Status")
st.plotly_chart(fig3, use_container_width=True)

# External Scores by TARGET
st.subheader("External Scores by Default Status")
avg_scores = df.groupby("TARGET")[["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"]].mean().reset_index()
fig4 = px.bar(avg_scores, x="TARGET", y=["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"], barmode="group",
              title="Average External Scores by Default Status")
st.plotly_chart(fig4, use_container_width=True)

# EXT_SOURCE_1 vs EXT_SOURCE_2
st.subheader("EXT_SOURCE_1 vs EXT_SOURCE_2")
fig5 = px.scatter(df, x="EXT_SOURCE_1", y="EXT_SOURCE_2", color="TARGET", opacity=0.5,
                  title="EXT_SOURCE_1 vs EXT_SOURCE_2")
st.plotly_chart(fig5, use_container_width=True)

# EXT_SOURCE_2 vs EXT_SOURCE_3
st.subheader("EXT_SOURCE_2 vs EXT_SOURCE_3")
fig6 = px.scatter(df, x="EXT_SOURCE_2", y="EXT_SOURCE_3", color="TARGET", opacity=0.5,
                  title="EXT_SOURCE_2 vs EXT_SOURCE_3")
st.plotly_chart(fig6, use_container_width=True)

# External Score vs Default Rate
st.subheader("Default Rate by Average External Score")
df["AvgExternalScore"] = df[["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"]].mean(axis=1)
df["Score_Bin"] = pd.cut(df["AvgExternalScore"], bins=10)
df["Score_Bin"] = df["Score_Bin"].astype(str)   # ✅ convert Interval to string
score_default = df.groupby("Score_Bin")["TARGET"].mean().reset_index()
fig7 = px.bar(score_default, x="Score_Bin", y="TARGET", title="Default Rate (%) by Avg External Score")
st.plotly_chart(fig7, use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3","AvgExternalScore","Score_Bin"]].head(20))
