import streamlit as st
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="COVID-19 Analytics Dashboard",
    layout="wide"
)

st.title("🌍 COVID-19 Analytics Dashboard")
st.markdown("Interactive Data Analysis using Python & Streamlit")

# -----------------------------
# Load Dataset
# -----------------------------
import os

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "covid_data.csv")
    df = pd.read_csv(file_path, parse_dates=["Date"])
    return df

df = load_data()

# -----------------------------
# Global Overview
# -----------------------------
st.header("🌎 Global Overview")

global_data = df.groupby("Date")[["Confirmed", "Deaths", "Recovered"]].sum()
latest_global = global_data.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total Confirmed", f"{latest_global['Confirmed']:,}")
col2.metric("Total Deaths", f"{latest_global['Deaths']:,}")
col3.metric("Total Recovered", f"{latest_global['Recovered']:,}")

# Global Trend Chart
st.subheader("📈 Global Trend Over Time")

fig_global, ax_global = plt.subplots(figsize=(12,5))
ax_global.plot(global_data.index, global_data["Confirmed"], label="Confirmed")
ax_global.plot(global_data.index, global_data["Deaths"], label="Deaths")
ax_global.plot(global_data.index, global_data["Recovered"], label="Recovered")

ax_global.set_xlabel("Date")
ax_global.set_ylabel("Cases")
ax_global.legend()
ax_global.grid(True)

st.pyplot(fig_global)

# -----------------------------
# Sidebar - Country Selection
# -----------------------------
st.sidebar.header("Filter Options")
countries = sorted(df["Country"].unique())
selected_country = st.sidebar.selectbox("Select Country", countries)

# -----------------------------
# Country Analysis
# -----------------------------
st.header(f"📊 Country Analysis: {selected_country}")

country_data = df[df["Country"] == selected_country].copy()
country_data = country_data.sort_values("Date")

# Add Death Rate %
country_data["Death Rate (%)"] = (
    country_data["Deaths"] / country_data["Confirmed"]
) * 100

# Add 7-Day Moving Average
country_data["MA7"] = country_data["Confirmed"].rolling(7).mean()

# Latest Country Metrics
latest = country_data.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Confirmed", f"{latest['Confirmed']:,}")
col2.metric("Deaths", f"{latest['Deaths']:,}")
col3.metric("Recovered", f"{latest['Recovered']:,}")

# -----------------------------
# Country Trend Chart
# -----------------------------
st.subheader("📈 Confirmed Cases with 7-Day Moving Average")

fig_country, ax_country = plt.subplots(figsize=(12,5))
ax_country.plot(country_data["Date"], country_data["Confirmed"], label="Confirmed")
ax_country.plot(country_data["Date"], country_data["MA7"], linestyle="--", label="7-Day MA")

ax_country.set_xlabel("Date")
ax_country.set_ylabel("Cases")
ax_country.legend()
ax_country.grid(True)

st.pyplot(fig_country)

# -----------------------------
# Death Rate Trend
# -----------------------------
st.subheader("⚠️ Death Rate (%) Trend")

fig_death, ax_death = plt.subplots(figsize=(12,5))
ax_death.plot(country_data["Date"], country_data["Death Rate (%)"], label="Death Rate (%)")

ax_death.set_xlabel("Date")
ax_death.set_ylabel("Death Rate (%)")
ax_death.legend()
ax_death.grid(True)

st.pyplot(fig_death)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Python, Pandas, Matplotlib & Streamlit")