import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data from the specified file
def load_data(file_name):
    file_path = os.path.join("index_data", f"{file_name}.xlsx")
    print(f"Loading data from file: {file_path}")
    return pd.read_excel(file_path)

# Get the list of files in the folder
file_names = [
    "^NSEBANK", "^NSEI", "^INDIAVIX", "^CNXPHARMA", "^CNXMEDIA",
    "^CNXAUTO", "^NSEDIV", "^CNXSC", "^CNXFMCG", "^CNXCONSUM",
    "^CNXDIVOP", "^CNXMETAL", "^CNXIT", "^CNXREALTY", "^NSEI",
    "^CNXMNC", "^CRSLDX", "^CNXCMDT", "^CNX100", "^CNXINFRA",
    "^CNX200", "^BSESN", "^CNXENERGY", "^CNXSERVICE", "^CNXPSE",
    "^NSEMDCP50", "^NSMIDCP", "^NSEBANK", "^CNXFIN", "^CNXPSUBANK"
]

# Sidebar
st.sidebar.header("Stock Comparison")
start_date = st.sidebar.date_input("Select start date")
end_date = st.sidebar.date_input("Select end date")

selected_stocks = st.sidebar.multiselect("Select stocks", file_names)

# Load data for selected stocks
data = {stock: load_data(stock) for stock in selected_stocks}

# Merge data on 'Date' column
merged_data = pd.concat([data[stock].set_index('Date')[['Adj Close']].rename(columns={'Adj Close': stock}) for stock in selected_stocks], axis=1)

# Filter data based on user input
filtered_data = merged_data[(merged_data.index >= start_date) & (merged_data.index <= end_date)]

# Normalize data if required
normalize_data = st.sidebar.checkbox("Normalize data")
if normalize_data:
    filtered_data = filtered_data / filtered_data.iloc[0] * 100

# Line chart
fig = px.line(filtered_data, labels={'value': 'Stock Value'})
fig.update_layout(title='Stock Comparison', xaxis_title='Date', yaxis_title='Stock Value')

# Show chart
st.plotly_chart(fig)
