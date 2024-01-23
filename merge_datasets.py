import os
import pandas as pd

csv_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.csv')]

concatenated_data = pd.DataFrame()

for csv_file in csv_files:
    file_path = os.path.join(os.getcwd(), csv_file)
    data = pd.read_csv(file_path)
    concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)

concatenated_data.to_csv(os.path.join(os.getcwd(), "merged_dataset.csv"), index=False)