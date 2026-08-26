import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY",
        "EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3",
        "DAYS_BIRTH","DAYS_EMPLOYED","CNT_CHILDREN","CNT_FAM_MEMBERS"
    ])
    # Derived features
    df["AGE"] = (df["DAYS_BIRTH"].abs()/365).astype(int)
    df["EmploymentYears"] = (df["DAYS_EMPLOYED"].abs()/365).astype(int)
    df["CreditIncomeRatio"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    df["AnnuityIncomeRatio"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
    df["AvgExternalScore"] = df[["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"]].mean(axis=1)
    return df

df = load_data()

st.title("🔗 Correlation & Risk Factor Analysis")

# Correlation Heatmap
st.subheader("Correlation Heatmap")
corr = df.corr(numeric_only=True)
fig1 = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
st.plotly_chart(fig1, use_container_width=True)

# Correlation with TARGET
st.subheader("Correlation with TARGET")
target_corr = corr["TARGET"].drop("TARGET").sort_values()
fig2 = px.bar(target_corr, x=target_corr.index, y=target_corr.values, title="Correlation with Default (TARGET)")
st.plotly_chart(fig2, use_container_width=True)

# Top Positive Correlations
st.subheader("Top Positive Correlations with TARGET")
top_pos = target_corr.sort_values(ascending=False).head(5)
fig3 = px.bar(top_pos, x=top_pos.index, y=top_pos.values, title="Top Positive Correlations")
st.plotly_chart(fig3, use_container_width=True)

# Top Negative Correlations
st.subheader("Top Negative Correlations with TARGET")
top_neg = target_corr.sort_values(ascending=True).head(5)
fig4 = px.bar(top_neg, x=top_neg.index, y=top_neg.values, title="Top Negative Correlations")
st.plotly_chart(fig4, use_container_width=True)

# Credit vs Income Scatter Plot
st.subheader("Credit vs Income Scatter Plot")
fig5 = px.scatter(df, x="AMT_INCOME_TOTAL", y="AMT_CREDIT", color="TARGET", opacity=0.5,
                  title="Credit vs Income (Risk Overlay)")
st.plotly_chart(fig5, use_container_width=True)

# External Score vs TARGET
st.subheader("External Score vs Default")
fig6 = px.box(df, x="TARGET", y="AvgExternalScore", color="TARGET", title="External Score vs Default")
st.plotly_chart(fig6, use_container_width=True)

# Important Risk Factors Section
st.subheader("Potential Risk Indicators")
risk_factors = {
    "Low External Credit Score (<0.3)": (df["AvgExternalScore"]<0.3).mean()*100,
    "High Credit-to-Income Ratio (>6)": (df["CreditIncomeRatio"]>6).mean()*100,
    "High Annuity-to-Income Ratio (>0.3)": (df["AnnuityIncomeRatio"]>0.3).mean()*100,
    "Younger Age (<30)": (df["AGE"]<30).mean()*100,
    "Short Employment (<2 years)": (df["EmploymentYears"]<2).mean()*100
}
risk_df = pd.DataFrame(list(risk_factors.items()), columns=["Risk Factor","% Customers"])
st.dataframe(risk_df)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df.head(20))
