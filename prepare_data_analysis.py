import os
import shutil
import zipfile
from utils import *

#Converting noise levels data to minutes data
noise_levels_merged_folder = 'noise_levels_parquets'
noise_levels_min_folder = 'noise_levels_min_parquets'
if not os.path.exists(noise_levels_min_folder):
    os.mkdir(noise_levels_min_folder)
for file in os.listdir(noise_levels_merged_folder):
    output_folder = os.path.join(noise_levels_min_folder, file)
    parquet_file_path = os.path.join(noise_levels_merged_folder, file)
    sec_to_min(parquet_file_path, output_folder)
#Merging the minutes noise levels for all the months to get a single file
print('Merging Noise Minutes Data...')
minutes_data_path = 'noise_minutes.parquet'
if not os.path.isfile(minutes_data_path):
    merge_parquet_files(noise_levels_min_folder, minutes_data_path)

print(f'Noise Minutes Data Downloaded and Merged into {minutes_data_path}.')
shutil.rmtree(noise_levels_min_folder)