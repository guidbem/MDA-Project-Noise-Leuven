import gdown
import polars as pl
import os
import glob


def download_gdrive_folder(url: str, output: str=None):
    """
    Downloads a folder from Google Drive.

    Parameters:
        - url       : The google drive folder url
        - output    : The local folder name (optional, takes the gdrive folder name if none is given)
    """
    try:
        gdown.download_folder(url, quiet=True, use_cookies=False, output=output)

    except:
        print('Download Failed, check if gdrive folder link is valid')

def merge_csv_files(
        folder_path: str, 
        output_path: str, 
        sep: str=',', 
        infer_schema_length: int=1000,
        null_values: list=['', 'null', 'NULL', 'Null', 'NaN', 'nan', 'NA', 'na', 'N/A', 'n/a']
        ):
    """
    Merges all csv files in a folder into a single csv file using the polars library.

    Parameters:
        - folder_path   : The folder path containing the csv files
        - output_path   : The output path for the merged csv file
    """
    # Get all csv files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    
    # Read all csv files into polars dataframes
    dfs = []
    for csv_file in csv_files:
        df = pl.read_csv(
                csv_file,
                separator=sep,
                infer_schema_length=infer_schema_length,
                null_values=null_values
                )
        
        if df.shape[0] > 0:
            dfs.append(df)

    # Concatenate all dataframes
    df = pl.concat(dfs)

    # Write the dataframe to a csv file
    df.write_parquet(output_path)

def merge_parquet_files(
        folder_path: str, 
        output_path: str
        ):
    """
    Merges all parquet files in a folder into a single parquet file using the polars library.

    Parameters:
        - folder_path   : The folder path containing the parquet files
        - output_path   : The output path for the merged parquet file
    """
    # Get all parquet files in the folder
    parquet_files = glob.glob(os.path.join(folder_path, '*.parquet'))
    
    # Read all parquet files into polars dataframes
    dfs = []
    
    for parquet_file in parquet_files:
        df = pl.read_parquet(parquet_file)
        
        if df.shape[0] > 0:
            dfs.append(df)

    # Concatenate all dataframes
    df = pl.concat(dfs)

    # Write the dataframe to a parquet file
    df.write_parquet(output_path)