import pandas as pd
import os

def load_country_data(country_name):
    filepath = f"../../data/{country_name}_Solar_Data.csv"
    df = pd.read_csv(filepath, parse_dates=['Timestamp'])
    df['Country'] = country_name
    return df

def merge_selected_countries(country_list):
    dfs = [load_country_data(country) for country in country_list]
    return pd.concat(dfs, ignore_index=True)
