import os
import shutil
import zipfile
from utils import *

#Converting noise levels data to minutes data
noise_levels_merged_folder = 'data/noise_levels_parquets'
noise_levels_min_folder = 'data/noise_levels_min_parquets'
if not os.path.exists(noise_levels_min_folder):
    os.mkdir(noise_levels_min_folder)
for file in os.listdir(noise_levels_merged_folder):
    output_folder = os.path.join(noise_levels_min_folder, file)
    parquet_file_path = os.path.join(noise_levels_merged_folder, file)
    sec_to_min(parquet_file_path, output_folder)
#Merging the minutes noise levels for all the months to get a single file
print('Merging Noise Minutes Data...')
minutes_data_path = 'data/noise_minutes.parquet'
if not os.path.isfile(minutes_data_path):
    merge_parquet_files(noise_levels_min_folder, minutes_data_path)

print(f'Noise Minutes Data Downloaded and Merged into {minutes_data_path}.')
shutil.rmtree(noise_levels_min_folder)

# Read the Parquet file into a pandas DataFrame
df_parquet = pd.read_parquet('data/noise_events.parquet')

# Convert the DataFrame to CSV format
df_parquet.to_csv('data/merged.csv', index=False)

# Reading the csv

df = pd.read_csv("data/merged.csv")

# Only the required columns are selected

df = df[['#object_id', 'description', 'result_timestamp', 'noise_event_laeq_primary_detected_class']]

# Changing the NAs

df['noise_event_laeq_primary_detected_class'].fillna("Not Available", inplace=True)

# creating the doughnut_data.csv

df.to_csv('data/doughnut_data.csv', index=False)