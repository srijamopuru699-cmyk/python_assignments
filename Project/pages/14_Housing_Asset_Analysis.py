import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv", usecols=[
        "SK_ID_CURR","TARGET","FLAG_OWN_CAR","FLAG_OWN_REALTY",
        "NAME_HOUSING_TYPE","AMT_CREDIT"
    ])
    return df

df = load_data()

st.title("🏠 Page 14 – Housing & Asset Analysis")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Car Owners", (df["FLAG_OWN_CAR"]=="Y").sum())
col2.metric("Property Owners", (df["FLAG_OWN_REALTY"]=="Y").sum())
col3.metric("Customers Owning Both", ((df["FLAG_OWN_CAR"]=="Y") & (df["FLAG_OWN_REALTY"]=="Y")).sum())
col4.metric("Default Rate of Property Owners", f"{df.loc[df['FLAG_OWN_REALTY']=='Y','TARGET'].mean()*100:.2f}%")

# Visualization 1: Car Ownership Distribution
st.subheader("Car Ownership Distribution")
fig1 = px.histogram(df, x="FLAG_OWN_CAR", color="TARGET", barmode="group",
                    title="Car Ownership Distribution by Default Status")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Property Ownership Distribution
st.subheader("Property Ownership Distribution")
fig2 = px.histogram(df, x="FLAG_OWN_REALTY", color="TARGET", barmode="group",
                    title="Property Ownership Distribution by Default Status")
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Default Rate by Car Ownership
st.subheader("Default Rate by Car Ownership")
car_default = df.groupby("FLAG_OWN_CAR")["TARGET"].mean().reset_index()
fig3 = px.bar(car_default, x="FLAG_OWN_CAR", y="TARGET", title="Default Rate by Car Ownership")
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Default Rate by Property Ownership
st.subheader("Default Rate by Property Ownership")
prop_default = df.groupby("FLAG_OWN_REALTY")["TARGET"].mean().reset_index()
fig4 = px.bar(prop_default, x="FLAG_OWN_REALTY", y="TARGET", title="Default Rate by Property Ownership")
st.plotly_chart(fig4, use_container_width=True)

# Visualization 5: Applicants by Housing Type
st.subheader("Applicants by Housing Type")
fig5 = px.histogram(df, x="NAME_HOUSING_TYPE", color="TARGET", barmode="group",
                    title="Applicants by Housing Type")
st.plotly_chart(fig5, use_container_width=True)

# Visualization 6: Default Rate by Housing Type
st.subheader("Default Rate by Housing Type")
housing_default = df.groupby("NAME_HOUSING_TYPE")["TARGET"].mean().reset_index()
fig6 = px.bar(housing_default, x="NAME_HOUSING_TYPE", y="TARGET", title="Default Rate by Housing Type")
st.plotly_chart(fig6, use_container_width=True)

# Visualization 7: Average Credit by Housing Type
st.subheader("Average Credit by Housing Type")
housing_credit = df.groupby("NAME_HOUSING_TYPE")["AMT_CREDIT"].mean().reset_index()
fig7 = px.bar(housing_credit, x="NAME_HOUSING_TYPE", y="AMT_CREDIT", title="Average Credit by Housing Type")
st.plotly_chart(fig7, use_container_width=True)

# Sample Records
st.subheader("Sample Customer Records")
st.dataframe(df[["SK_ID_CURR","TARGET","FLAG_OWN_CAR","FLAG_OWN_REALTY","NAME_HOUSING_TYPE","AMT_CREDIT"]].head(20))
