import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

def tail_file(file_path):
    """Generator function that yields new lines in a file."""
    with open(file_path, 'r') as file:
        file.seek(0, 2)  # Move the cursor to the end of the file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly to avoid busy waiting
                continue
            yield line

def load_data(file_path, skip_rows):
    """Load only new data from the file."""
    for line in tail_file(file_path):
        if line.strip():  # This checks if the line is not just a newline
            # Create a DataFrame from a single line
            data = pd.read_csv(pd.io.common.StringIO(line), sep="\t",
                               names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"],
                               usecols=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"])
            data = data.apply(pd.to_numeric, errors='coerce').dropna()
            if not data.empty:
                yield data

def plot_real_time_temperatures(file_path):
    st.title("Real-Time Temperature Monitoring")
    st.write("Reading temperature data...")

    plot_placeholder = st.empty()
    initial_skip = True

    time_points = []
    temp_0_points, temp_1_points, temp_2_points = [], [], []

    for new_data in load_data(file_path, skip_initial_headers=True):
        for index, row in new_data.iterrows():
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
            plt.grid()

            plot_placeholder.pyplot(plt)
            plt.close()

            time.sleep(1)  # Update rate might be adjusted based on actual data rate

file_path = './exp12.lvm'  # Ensure this is the correct path to your continuously updating file

# Run the app
try:
    plot_real_time_temperatures(file_path)
except Exception as e:
    st.error(f"An error occurred: {e}")
