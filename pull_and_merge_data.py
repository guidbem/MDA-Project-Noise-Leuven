import os
import shutil
import zipfile
from utils import download_gdrive_folder, merge_csv_files, convert_utc_to_cest_meteo


######### METEO DATA #########
# Download the Meteo Data (Q1-Q4 csv files in Google Drive)
print('Downloading Meteo Data...')
folder_meteo_data = 'meteo_data'
if not os.path.exists(folder_meteo_data):
    download_gdrive_folder(
        url="https://drive.google.com/drive/folders/1pyhwyBj2bh5WTZEu67xPYqZjF5OcECF5",
        output=folder_meteo_data
    )
else:
    print(f'{folder_meteo_data} folder already exists.')

# Merge the Meteo Data into a single parquet file
print('Merging Meteo Data...')
meteo_data_path = 'meteo_data.parquet'
if not os.path.isfile(meteo_data_path):
    merge_csv_files(folder_meteo_data, meteo_data_path)

print(f'Meteo Data Downloaded and Merged into {meteo_data_path}.')
# Adjust the timezone from UTC to CEST
print('Adjusting Meteo Data Timezone from UTC to CEST...')
convert_utc_to_cest_meteo(meteo_data_path)
shutil.rmtree(folder_meteo_data)

######### NOISE PERCENTILE AND EVENTS DATA #########
# Download the Noise Percentile and Events Data (year zip files in google drive folder)
print('Downloading Noise Percentile and Events Data...')
tmp_folder = 'tmp'
folder_percentiles_data = 'noise_percentiles'
folder_events_data = 'noise_events'
if not os.path.exists(folder_percentiles_data) and not os.path.exists(folder_events_data):
    download_gdrive_folder(
        url="https://drive.google.com/drive/folders/17NrwOWm8-zvIv5J7keAjTPqWiH1CjQzf",
        output=tmp_folder
    )
    # List all zip files in the Noise Percentile and Events folder and unzip them
    print('Download Succesfull, Now Unzipping Noise Percentile and Events Data...')
    zip_files = [f for f in os.listdir(tmp_folder) if f.endswith('.zip')]
    for zip_file in zip_files:
        zip_path = os.path.join(tmp_folder, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zipObj:
            # extract all files into specified directory
            if zip_file == 'export_40.zip': 
                extract_path = folder_percentiles_data
            elif zip_file == 'export_41.zip':
                extract_path = folder_events_data

            zipObj.extractall(extract_path)
            
    # Delete the folder with the zip files
    shutil.rmtree(tmp_folder)

else:
    print(f'{folder_percentiles_data} and {folder_events_data} folders already exists.')

# Merge the Noise Percentile Data into a single parquet file
print('Merging Noise Percentile Data...')
percentiles_data_path = 'noise_percentiles.parquet'
if not os.path.isfile(percentiles_data_path):
    merge_csv_files(folder_percentiles_data, percentiles_data_path, sep=';')

print(f'Noise Percentile Data Downloaded and Merged into {percentiles_data_path}.')
shutil.rmtree(folder_percentiles_data)

# Merge the Noise Events Data into a single parquet file
print('Merging Noise Events Data...')
events_data_path = 'noise_events.parquet'
if not os.path.isfile(events_data_path):
    merge_csv_files(folder_events_data, events_data_path, sep=';', infer_schema_length=2000)

print(f'Noise Events Data Downloaded and Merged into {events_data_path}.')
shutil.rmtree(folder_events_data)

######### NOISE LEVELS DATA #########
# Download the Noise Levels Data (month zip files in google drive folder)
print('Downloading Noise Levels Data (can take a while)...')
folder_levels_data = 'noise_levels'
if not os.path.exists(folder_levels_data):
    download_gdrive_folder(
        url = "https://drive.google.com/drive/folders/1HT-ctj8Aj6qcVMZYBxi3YM4XC9fbFjSN",
        output=folder_levels_data
    )
    print('Download Succesfull, Now Unzipping Noise Levels Data...')
    # List all zip files in the Noise Levels folder and unzip them
    zip_files = [f for f in os.listdir(folder_levels_data) if f.endswith('.zip')]
    for zip_file in zip_files:
        zip_path = os.path.join(folder_levels_data, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zipObj:
            # extract all files into specified directory
            zipObj.extractall(zip_path[:-4])

        # Delete the zip file
        os.remove(zip_path)

else:
    print(f'{folder_levels_data} folder already exists.')

# Merge the Months Noise Levels Data into a single parquet files
noise_levels_merged_folder = 'noise_levels_parquets'
if not os.path.exists(noise_levels_merged_folder):
    os.mkdir(noise_levels_merged_folder)
print('Merging Noise Levels Data...')
for folder in os.listdir(folder_levels_data):
    folder_path = os.path.join(folder_levels_data, folder)
    out_path = os.path.join(noise_levels_merged_folder, folder+'.parquet')
    merge_csv_files(folder_path, out_path, sep=';')

print(f'Noise Levels Data Downloaded and Merged into {noise_levels_merged_folder}.')
shutil.rmtree(folder_levels_data)