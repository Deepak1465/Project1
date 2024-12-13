def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Print to check the lines read
        for i, line in enumerate(lines[:10]):  # Let's print the first 10 lines
            print(f"Line {i}: {line.strip()}")

        header_marker = "***End_of_Header***"
        data_start_line = next(i for i, line in enumerate(lines) if header_marker in line) + 1
        print(f"Header ends at line: {data_start_line}")

        for i, line in enumerate(lines[data_start_line:]):
            if "X_Value" in line:
                actual_data_start = data_start_line + i + 1
                break
        print(f"Actual data starts at line: {actual_data_start}")

        # Load data into a DataFrame
        data = pd.read_csv(
            file_path,
            sep="\t",
            skiprows=actual_data_start - 1,
            names=["X_Value", "Temperature_0", "Temperature_1", "Temperature_2"]
        )

        # Print loaded data
        print(f"Loaded data: {data.head()}")

        # Convert columns to numeric, replacing invalid values with NaN
        data = data.apply(pd.to_numeric, errors='coerce')

        # Drop rows with NaN values
        data.dropna(inplace=True)

        if data.empty:
            print("No valid data found after processing.")

        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame to handle errors gracefully

# Adjust the file path as needed and run the app
file_path = './exp12.lvm'  # or use the absolute path if unsure about the relative path
