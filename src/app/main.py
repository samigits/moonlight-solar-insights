import streamlit as st
import pandas as pd
from utils import merge_selected_countries
import seaborn as sns
import matplotlib.pyplot as plt

# Load selected countries
country_options = ["Benin", "SierraLeone", "Togo"]  # add actual filenames in /data
selected_countries = st.sidebar.multiselect("Choose 2 or 3 countries", country_options, default=["Benin", "Togo"])

if len(selected_countries) < 2 or len(selected_countries) > 3:
    st.warning("Please select 2 or 3 countries.")
    st.stop()

df = merge_selected_countries(selected_countries)

# Date range slider
df['Timestamp'] = pd.to_datetime(df['Timestamp'])  # ensure Timestamp is datetime
min_date = df['Timestamp'].min().date()
max_date = df['Timestamp'].max().date()

start_date, end_date = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Filter by date range
filtered_df = df[
    (df['Timestamp'] >= pd.to_datetime(start_date)) & 
    (df['Timestamp'] <= pd.to_datetime(end_date))
]

# Now use filtered_df for all plots below
st.subheader("GHI Over Time")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="Timestamp", y="GHI", hue="Country", ax=ax)
st.pyplot(fig)

# DNI comparison
st.subheader("DNI Over Time")
fig_dni, ax_dni = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="Timestamp", y="DNI", hue="Country", ax=ax_dni)
st.pyplot(fig_dni)

# DHI comparison
st.subheader("DHI Over Time")
fig_dhi, ax_dhi = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="Timestamp", y="DHI", hue="Country", ax=ax_dhi)
st.pyplot(fig_dhi)

st.subheader("Bubble Chart: GHI vs DNI (Bubble Size = DHI)")

fig_bubble, ax_bubble = plt.subplots(figsize=(10, 6))

for country in filtered_df['Country'].unique():
    subset = filtered_df[filtered_df['Country'] == country]
    ax_bubble.scatter(
        subset["GHI"], 
        subset["DNI"], 
        s=subset["DHI"] / 5,  # scale down bubble size
        alpha=0.5, 
        label=country
    )

ax_bubble.set_xlabel("GHI (W/m²)")
ax_bubble.set_ylabel("DNI (W/m²)")
ax_bubble.set_title("GHI vs DNI with DHI as Bubble Size")
ax_bubble.legend(title="Country")
st.pyplot(fig_bubble)


# Average Metric Bar Chart by Country
st.subheader("Average GHI, DNI, DHI per Country")
avg_df = filtered_df.groupby("Country")[["GHI", "DNI", "DHI"]].mean().reset_index()
avg_chart = avg_df.set_index("Country").plot(kind="bar", figsize=(8, 4))
st.pyplot(avg_chart.figure)
