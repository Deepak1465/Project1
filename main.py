import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import io

def tail_file(file_path):
    """Yield new lines added to file."""
    with open(file_path, 'r') as file:
        # Start reading the file at the end
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

def check_data_stream(file_path):
    """Check new data being read from the file."""
    st.write("Checking data stream...")
    try:
        for line in tail_file(file_path):
            if line.strip():
                st.write(f"New line: {line.strip()}")
                yield line
    except Exception as e:
        st.error(f"Failed during data streaming: {e}")

def main(file_path):
    st.title("Real-Time Data Streaming Check")

    for line in check_data_stream(file_path):
        try:
            # Simulate data processing
            data = pd.read_csv(io.StringIO(line), sep="\t",
                               names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"],
                               usecols=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"])
            data = data.apply(pd.to_numeric, errors='coerce').dropna()
            if not data.empty:
                st.write(data)
            else:
                st.write("Processed data is empty or invalid.")
        except Exception as e:
            st.error(f"Error processing a line: {e}")

if __name__ == "__main__":
    file_path = './exp12.lvm'  # Ensure this is the correct path to your continuously updating file
    try:
        main(file_path)
    except Exception as e:
        st.error(f"An error occurred: {e}")
