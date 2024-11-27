import streamlit as st
import pandas as pd
import time

# Define a function to load data after the "***End_of_Header***" marker
def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the actual start of the data
    header_marker = "***End_of_Header***"
    data_start_line = next(i for i, line in enumerate(lines) if header_marker in line) + 1

    for i, line in enumerate(lines[data_start_line:]):
        if "X_Value" in line:
            actual_data_start = data_start_line + i + 1
            break

    # Load data into a DataFrame
    data = pd.read_csv(
        file_path,
        sep="\t",
        skiprows=actual_data_start - 1,
        names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2", "Comment"],
        usecols=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"]
    )

    # Convert columns to numeric, replacing invalid values with NaN
    data = data.apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN values
    data.dropna(inplace=True)

    return data

# Streamlit app for displaying current temperatures
def display_real_time_temperatures(file_path):
    st.title("Real-Time Temperature Monitoring")
    st.write(f"Reading temperature data from: `{file_path}`")

    # Load the data
    data = load_data(file_path)

    # Create three columns for displaying temperatures
    col1, col2, col3 = st.columns(3)

    # Real-time loop to display temperatures
    for index, row in data.iterrows():
        # Get the current temperatures
        temp_0, temp_1, temp_2 = row["Temperature_0"], row["Temperature_1"], row["Temperature_2"]

        # Update current temperatures in the three columns
        col1.metric("Temperature_0", f"{temp_0:.2f} °C")
        col2.metric("Temperature_1", f"{temp_1:.2f} °C")
        col3.metric("Temperature_2", f"{temp_2:.2f} °C")

        # Wait for 1 second to simulate real-time updates
        time.sleep(1)

# File path for the .lvm file
file_path = './exp12.lvm'

# Run the app
try:
    display_real_time_temperatures(file_path)
except Exception as e:
    st.error(f"An error occurred: {e}")
