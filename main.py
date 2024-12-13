import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# Define a function to load data after the "***End_of_Header***" marker
def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the actual start of the data
    header_marker = "***End_of_Header***"
    data_start_line = next(i for i, line in enumerate(lines) if header_marker in line) + 1

    # Find the start of the actual data after the header
    for i, line in enumerate(lines[data_start_line:]):
        if "X_Value" in line:
            actual_data_start = data_start_line + i + 1
            break

    # Load data into a DataFrame
    data = pd.read_csv(
        file_path,
        sep="\t",
        skiprows=actual_data_start - 1,
        names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"]
    )

    # Convert columns to numeric, replacing invalid values with NaN
    data = data.apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN values
    data.dropna(inplace=True)

    return data

# Streamlit app for plotting temperatures
def plot_real_time_temperatures(file_path):
    st.title("Real-Time Temperature Monitoring")
    st.write(f"Reading temperature data from: `{file_path}`")

    # Load the data
    data = load_data(file_path)
    data["X_Value"] = data["X_Value"].cumsum()  # Simulate time increment

    # Initialize plot placeholder
    plot_placeholder = st.empty()

    # Initialize lists to hold the data points for plotting
    time_points = []
    temp_0_points, temp_1_points, temp_2_points = [], [], []

    # Real-time plotting loop
    for index, row in data.iterrows():
        # Append new data points to the lists
        time_points.append(row["X_Value"])
        temp_0_points.append(row["Temperature_0"])
        temp_1_points.append(row["Temperature_1"])
        temp_2_points.append(row["Temperature_2"])

        # Clear the previous figure to avoid memory overflow
        plt.clf()

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, temp_0_points, label="Temperature_0", color="red")
        plt.plot(time_points, temp_1_points, label="Temperature_1", color="blue")
        plt.plot(time_points, temp_2_points, label="Temperature_2", color="green")
        plt.title("Real-Time Temperature Plot")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.tight_layout()

        # Display the plot in the Streamlit app
        plot_placeholder.pyplot(plt)

        # Simulate real-time update delay
        time.sleep(1)

# File path for the .lvm file
file_path = './exp12.lvm'

# Run the app
try:
    plot_real_time_temperatures(file_path)
except Exception as e:
    st.error(f"An error occurred: {e}")
