import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        header_marker = "***End_of_Header***"
        data_start_line = next(i for i, line in enumerate(lines) if header_marker in line) + 1
        actual_data_start = data_start_line + next(i for i, line in enumerate(lines[data_start_line:]) if "X_Value" in line) + 1

        data = pd.read_csv(
            file_path,
            sep="\t",
            skiprows=actual_data_start - 1,
            names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"]
        )
        data = data.apply(pd.to_numeric, errors='coerce')
        data.dropna(inplace=True)

        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

def plot_real_time_temperatures(file_path):
    st.title("Real-Time Temperature Monitoring")
    st.write(f"Reading temperature data from: `{file_path}`")

    data = load_data(file_path)
    if data.empty:
        st.error("No data available to plot.")
        return

    data["X_Value"] = data["X_Value"].cumsum()

    plot_placeholder = st.empty()
    metrics_container = st.container()

    # Initialize metric elements outside the loop
    temp_0_metric = metrics_container.empty()
    temp_1_metric = metrics_container.empty()
    temp_2_metric = metrics_container.empty()

    time_points = []
    temp_0_points, temp_1_points, temp_2_points = [], [], []
    last_temp_0, last_temp_1, last_temp_2 = 0, 0, 0

    for index, row in data.iterrows():
        current_time = row["X_Value"]
        temp_0, temp_1, temp_2 = row["Temperature_0"], row["Temperature_1"], row["Temperature_2"]
        time_points.append(current_time)
        temp_0_points.append(temp_0)
        temp_1_points.append(temp_1)
        temp_2_points.append(temp_2)

        plt.figure(figsize=(10, 6))
        plt.plot(time_points, temp_0_points, label="Temperature 0", color="red")
        plt.plot(time_points, temp_1_points, label="Temperature 1", color="blue")
        plt.plot(time_points, temp_2_points, label="Temperature 2", color="green")
        plt.title("Real-Time Temperature Plot")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Temperature (°C)")
        plt.legend()

        plot_placeholder.pyplot(plt)
        plt.close()

        # Update metrics in the same place
        temp_0_metric.metric("Temperature 0", f"{temp_0:.2f} °C", f"{temp_0 - last_temp_0:.2f} °C")
        temp_1_metric.metric("Temperature 1", f"{temp_1:.2f} °C", f"{temp_1 - last_temp_1:.2f} °C")
        temp_2_metric.metric("Temperature 2", f"{temp_2:.2f} °C", f"{temp_2 - last_temp_2:.2f} °C")
        
        last_temp_0, last_temp_1, last_temp_2 = temp_0, temp_1, temp_2

        time.sleep(1)

file_path = './exp12.lvm'
try:
    plot_real_time_temperatures(file_path)
except Exception as e:
    st.error(f"An error occurred: {e}")
