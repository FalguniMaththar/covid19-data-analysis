import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/covid_data.csv", parse_dates=["Date"])

print("Data Overview:")
print(df.head())

# Group global data
global_trend = df.groupby("Date")[["Confirmed", "Deaths", "Recovered"]].sum()

# Add new features
global_trend["Death_Rate (%)"] = (global_trend["Deaths"] / global_trend["Confirmed"]) * 100
global_trend["Recovery_Rate (%)"] = (global_trend["Recovered"] / global_trend["Confirmed"]) * 100

# Moving Average (7-day)
global_trend["Confirmed_MA7"] = global_trend["Confirmed"].rolling(window=7).mean()

# Plot Global Trend
plt.figure(figsize=(12,6))
plt.plot(global_trend.index, global_trend["Confirmed"], label="Confirmed")
plt.plot(global_trend.index, global_trend["Confirmed_MA7"], label="7-Day Moving Avg", linestyle="--")
plt.plot(global_trend.index, global_trend["Deaths"], label="Deaths")
plt.plot(global_trend.index, global_trend["Recovered"], label="Recovered")

plt.title("Global COVID-19 Trend")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("images/global_trend.png")
plt.show()

print("\nLatest Global Statistics:")
print(global_trend.tail())