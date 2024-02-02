import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data from the specified file
def load_data(file_name):
    file_path = os.path.join("index_data", f"{file_name}_data.xlsx")
    try:
        print(f"Loading data from file: {file_path}")
        df = pd.read_excel(file_path)
        if 'Date' not in df.columns or 'Adj Close' not in df.columns:
            raise ValueError("Required columns ('Date' and 'Adj Close') not found in the DataFrame.")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return pd.DataFrame()

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

# Filter out any empty DataFrames
data = {key: value for key, value in data.items() if not value.empty}

# Check if there are any DataFrames to concatenate
if not data:
    st.warning("No valid data found for selected stocks. Please check your data files.")
else:
    # Merge data on 'Date' column
    try:
        merged_data = pd.concat([df.set_index('Date')[['Adj Close']].rename(columns={'Adj Close': stock}) for stock, df in data.items()], axis=1)
    except ValueError as e:
        st.error(f"Error during concatenation: {e}")
        st.error("Ensure that 'Date' column exists in all loaded DataFrames and there is data in the selected date range.")
        st.stop()

    # Convert date to datetime64[ns] for comparison
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

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
