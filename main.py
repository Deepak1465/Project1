import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
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

# Streamlit app for plotting maximum temperatures
def plot_real_time_temperatures(file_path):
    st.title("Real-Time Maximum Temperature Plot")
    st.write(f"Reading temperature data from: `{file_path}`")

    # Load the data
    data = load_data(file_path)
    data["X_Value"] = data["X_Value"].cumsum()  # Ensure X_Value increments by 1 second

    # Initialize variables
    max_temp_0, max_temp_1, max_temp_2 = float('-inf'), float('-inf'), float('-inf')
    time_points = []
    temp_0_points, temp_1_points, temp_2_points = [], [], []

    # Placeholder for the plot and metrics
    plot_placeholder = st.empty()
    temp_display_placeholder = st.container()

    # Real-time plotting loop
    for index, row in data.iterrows():
        # Update maximum temperatures
        current_time = row["X_Value"]
        temp_0, temp_1, temp_2 = row["Temperature_0"], row["Temperature_1"], row["Temperature_2"]

        # For each temperature column, update if a new max is reached or add a vertical line
        if temp_0 > max_temp_0:
            max_temp_0 = temp_0
        if temp_1 > max_temp_1:
            max_temp_1 = temp_1
        if temp_2 > max_temp_2:
            max_temp_2 = temp_2

        # Add points for plotting
        time_points.append(current_time)
        temp_0_points.append(max_temp_0)
        temp_1_points.append(max_temp_1)
        temp_2_points.append(max_temp_2)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, temp_0_points, label="Temperature_0", color="red")
        plt.plot(time_points, temp_1_points, label="Temperature_1", color="blue")
        plt.plot(time_points, temp_2_points, label="Temperature_2", color="green")

        # Add plot details
        plt.title("Real-Time Maximum Temperature Plot")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.grid()

        # Render the plot in Streamlit
        plot_placeholder.pyplot(plt)
        plt.close()

        # Update temperature metrics in Streamlit
        with temp_display_placeholder:
            st.metric(label="Temperature_0", value=f"{temp_0:.2f} °C")
            st.metric(label="Temperature_1", value=f"{temp_1:.2f} °C")
            st.metric(label="Temperature_2", value=f"{temp_2:.2f} °C")

        # Wait for 1 second to simulate real-time updates
        time.sleep(1)

# File path for the .lvm file
file_path = './exp12.lvm'

# Run the app
try:
    plot_real_time_temperatures(file_path)
except Exception as e:
    st.error(f"An error occurred: {e}")
