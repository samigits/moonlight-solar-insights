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

# ✅ Date range slider
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

# You can do the same for DNI, DHI, etc.
