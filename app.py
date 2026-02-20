import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("🌍 COVID-19 Analytics Dashboard")

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "covid_data.csv")
    return pd.read_csv(file_path, parse_dates=["Date"])

df = load_data()

# Global Overview
st.header("🌎 Global Overview")

global_data = df.groupby("Date")[["Confirmed", "Deaths", "Recovered"]].sum()
latest_global = global_data.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total Confirmed", f"{latest_global['Confirmed']:,}")
col2.metric("Total Deaths", f"{latest_global['Deaths']:,}")
col3.metric("Total Recovered", f"{latest_global['Recovered']:,}")

st.line_chart(global_data)

# Sidebar
st.sidebar.header("Filter Options")
countries = sorted(df["Country"].unique())
selected_country = st.sidebar.selectbox("Select Country", countries)

# Country Data
st.header(f"📊 Country Analysis: {selected_country}")

country_data = df[df["Country"] == selected_country].sort_values("Date")

country_data["Death Rate (%)"] = (
    country_data["Deaths"] / country_data["Confirmed"]
) * 100

country_data["MA7"] = country_data["Confirmed"].rolling(7).mean()

latest = country_data.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Confirmed", f"{latest['Confirmed']:,}")
col2.metric("Deaths", f"{latest['Deaths']:,}")
col3.metric("Recovered", f"{latest['Recovered']:,}")

st.subheader("Confirmed + Moving Average")
st.line_chart(country_data.set_index("Date")[["Confirmed", "MA7"]])

st.subheader("Death Rate Trend")
st.line_chart(country_data.set_index("Date")["Death Rate (%)"])