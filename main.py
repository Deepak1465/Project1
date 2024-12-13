# path_to_your_script.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

def tail_file(file_path):
    """Yield new lines added to file."""
    with open(file_path, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

def load_data(file_path):
    """Stream data from the file."""
    for line in tail_file(file_path):
        if line.strip():
            try:
                data = pd.read_csv(io.StringIO(line), sep="\t",
                                   names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"],
                                   usecols=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"])
                data = data.apply(pd.to_numeric, errors='coerce').dropna()
                if not data.empty:
                    yield data
            except Exception as e:
                st.error(f"Error processing data: {e}")

def main():
    st.title("Real-Time Data Streaming Check")
    file_path = './exp12.lvm'  # Update to your file path
    for new_data in load_data(file_path):
        st.write(new_data)
        plt.figure()
        plt.plot(new_data['X_Value'], new_data['Temperature_0'], label='Temp 0')
        plt.plot(new_data['X_Value'], new_data['Temperature_1'], label='Temp 1')
        plt.plot(new_data['X_Value'], new_data['Temperature_2'], label='Temp 2')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        st.pyplot(plt)

if __name__ == "__main__":
    main()
