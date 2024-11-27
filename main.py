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

# Streamlit app for plotting and displaying current temperatures
def plot_real_time_temperatures(file_path):
    st.title("Real-Time Temperature Monitoring")
    st.write(f"Reading temperature data from: `{file_path}`")

    # Load the data
    data = load_data(file_path)
    data["X_Value"] = data["X_Value"].cumsum()  # Ensure X_Value increments by 1 second

    # Placeholder for the plot
    plot_placeholder = st.empty()

    # Create three columns for displaying temperatures
    col1, col2, col3 = st.columns(3)

    # Real-time plotting loop
    for index, row in data.iterrows():
        # Get the current time and temperatures
        current_time = row["X_Value"]
        temp_0, temp_1, temp_2 = row["Temperature_0"], row["Temperature_1"], row["Temperature_2"]

        # Create the plot
        plt.figure(figsize=(8, 4))  # Smaller, minimal size
        plt.plot(data["X_Value"][:index+1], data["Temperature_0"][:index+1], label="Temperature_0", color="red", linewidth=1.5)
        plt.plot(data["X_Value"][:index+1], data["Temperature_1"][:index+1], label="Temperature_1", color="blue", linewidth=1.5)
        plt.plot(data["X_Value"][:index+1], data["Temperature_2"][:index+1], label="Temperature_2", color="green", linewidth=1.5)

        # Add minimal plot details
        plt.title("Temperature Trends", fontsize=14, fontweight='bold', loc='left', pad=10)
        plt.xlabel("Time (seconds)", fontsize=12)
        plt.ylabel("Temperature (°C)", fontsize=12)
        plt.legend(frameon=False, fontsize=10, loc="upper left")
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
        plt.tight_layout()  # Adjust layout to remove excess space

        # Hide top and right spines
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        # Render the plot in Streamlit
        plot_placeholder.pyplot(plt)
        plt.close()

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
    plot_real_time_temperatures(file_path)
except Exception as e:
    st.error(f"An error occurred: {e}")
