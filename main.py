import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# Define a function to load data after the "***End_of_Header***" marker
def load_data(file_path):
    try:
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
            names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"]
        )

        # Convert columns to numeric, replacing invalid values with NaN
        data = data.apply(pd.to_numeric, errors='coerce')

        # Drop rows with NaN values
        data.dropna(inplace=True)

        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame to handle errors gracefully

# Streamlit app for plotting temperatures
def plot_real_time_temperatures(file_path):
    st.title("Real-Time Temperature Monitoring")
    st.write(f"Reading temperature data from: `{file_path}`")

    # Load the data
    data = load_data(file_path)
    if data.empty:
        st.error("No data available to plot.")
        return

    data["X_Value"] = data["X_Value"].cumsum()  # Simulate time increment

    # Initialize plot placeholder
    plot_placeholder = st.empty()
    
    # Create a container for metrics
    metrics_container = st.container()

    # Initialize lists to hold the data points for plotting
    time_points = []
    temp_0_points, temp_1_points, temp_2_points = [], [], []
    last_temp_0, last_temp_1, last_temp_2 = 0, 0, 0  # Initialize last temperature values for delta calculation

    # Real-time plotting loop
    for index, row in data.iterrows():
        # Append new data points to the lists
        current_time = row["X_Value"]
        temp_0, temp_1, temp_2 = row["Temperature_0"], row["Temperature_1"], row["Temperature_2"]
        time_points.append(current_time)
        temp_0_points.append(temp_0)
        temp_1_points.append(temp_1)
        temp_2_points.append(temp_2)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, temp_0_points, label="Temperature 0", color="red")
        plt.plot(time_points, temp_1_points, label="Temperature 1", color="blue")
        plt.plot(time_points, temp_2_points, label="Temperature 2", color="green")
        plt.title("Real-Time Temperature Plot")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Temperature (°C)")
        plt.legend()

        # Display the plot in Streamlit
        plot_placeholder.pyplot(plt)
        plt.close()

        # Display metrics
        with metrics_container:
            st.metric(label="Temperature 0", value=f"{temp_0:.2f} °C", delta=f"{temp_0 - last_temp_0:.2f} °C")
            st.metric(label="Temperature 1", value=f"{temp_1:.2f} °C", delta=f"{temp_1 - last_temp_1:.2f} °C")
            st.metric(label="Temperature 2", value=f"{temp_2:.2f} °C", delta=f"{temp_2 - last_temp_2:.2f} °C")
        last_temp_0, last_temp_1, last_temp_2 = temp_0, temp_1, temp_2  # Update last temperatures

        # Wait for 1 second to simulate real-time updates
        time.sleep(1)

# File path for the .lvm file
file_path = './exp12.lvm'

# Run the app
try:
    plot_real_time_temperatures(file_path)
except Exception as e:
    st.error(f"An error occurred: {e}")
