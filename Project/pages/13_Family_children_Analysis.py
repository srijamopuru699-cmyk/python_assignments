import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","CNT_CHILDREN","CNT_FAM_MEMBERS","NAME_FAMILY_STATUS","AMT_INCOME_TOTAL"
    ])
    return df

df = load_data()

st.title("👨‍👩‍👧 Page 13 – Family & Children Analysis")

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Average Children", f"{df['CNT_CHILDREN'].mean():.2f}")
col2.metric("Average Family Members", f"{df['CNT_FAM_MEMBERS'].mean():.2f}")
col3.metric("Customers with Children", (df["CNT_CHILDREN"]>0).sum())
col4.metric("Customers without Children", (df["CNT_CHILDREN"]==0).sum())
# Highest Risk Family Type (based on default rate)
fam_status_default = df.groupby("NAME_FAMILY_STATUS")["TARGET"].mean().reset_index()
highest_risk_family = fam_status_default.loc[fam_status_default["TARGET"].idxmax(),"NAME_FAMILY_STATUS"]
col5.metric("Highest Risk Family Type", highest_risk_family)

# Visualization 1: Customers by Number of Children
st.subheader("Customers by Number of Children")
fig1 = px.histogram(df, x="CNT_CHILDREN", color="TARGET", nbins=20,
                    title="Customers by Number of Children")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Default Rate by Number of Children
st.subheader("Default Rate by Number of Children")
children_default = df.groupby("CNT_CHILDREN")["TARGET"].mean().reset_index()
fig2 = px.bar(children_default, x="CNT_CHILDREN", y="TARGET", title="Default Rate by Number of Children")
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Customers by Family Size
st.subheader("Customers by Family Size")
fig3 = px.histogram(df, x="CNT_FAM_MEMBERS", color="TARGET", nbins=20,
                    title="Customers by Family Size")
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Default Rate by Family Size
st.subheader("Default Rate by Family Size")
fam_default = df.groupby("CNT_FAM_MEMBERS")["TARGET"].mean().reset_index()
fig4 = px.bar(fam_default, x="CNT_FAM_MEMBERS", y="TARGET", title="Default Rate by Family Size")
st.plotly_chart(fig4, use_container_width=True)

# Visualization 5: Applications by Family Status
st.subheader("Applications by Family Status")
fig5 = px.histogram(df, x="NAME_FAMILY_STATUS", color="TARGET", barmode="group",
                    title="Applications by Family Status")
st.plotly_chart(fig5, use_container_width=True)

# Visualization 6: Default Rate by Family Status
st.subheader("Default Rate by Family Status")
fig6 = px.bar(fam_status_default, x="NAME_FAMILY_STATUS", y="TARGET", title="Default Rate by Family Status")
st.plotly_chart(fig6, use_container_width=True)

# Visualization 7: Income vs Family Size
st.subheader("Income vs Family Size")
fig7 = px.scatter(df, x="CNT_FAM_MEMBERS", y="AMT_INCOME_TOTAL", color="TARGET", opacity=0.5,
                  title="Income vs Family Size")
st.plotly_chart(fig7, use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","CNT_CHILDREN","CNT_FAM_MEMBERS","NAME_FAMILY_STATUS","AMT_INCOME_TOTAL"]].head(20))
