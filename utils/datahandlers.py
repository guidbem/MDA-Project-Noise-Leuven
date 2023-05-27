import gdown
import polars as pl
import os
import glob
import pandas as pd
import numpy as np


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

def convert_utc_to_cest_meteo(
    file_path: str
    ):
    """
    Converts all time values in a meteo parquet file from UTC to CEST.

    Parameters:
        - file_path   : The folder path containing the meteo parquet file
    """
    # Read the parquet file into a polars dataframe
    df = pd.read_parquet(file_path)

    # Convert the Hour column from UTC to CEST
    df['Hour'] = df['Hour'] + 2

    # Creates temporary Hour Column
    df['Hour_tmp'] = df['Hour']

    # Adjust invalid hour values
    df['Hour'] = np.where(df['Hour'] > 23, df['Hour'] - 24, df['Hour'])

    # Converts the date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Adjust days from invalid hour values
    df['Date'] = np.where(df['Hour_tmp'] > 23, df['Date'] + pd.DateOffset(1), df['Date'])
    df['Date'] = df['Date'].astype(str)

    # Drop the temporary Hour column
    df.drop(columns=['Hour_tmp'], inplace=True)

    # Write the dataframe to a parquet file
    df.to_parquet(file_path)

def sec_to_min(parquet_file_path: str, output_path: str):
    import polars as pl

    # Read the Parquet file using Polars
    sec = pl.read_parquet(parquet_file_path)

    # Split the result_timestamp column into date and time columns
    sec = sec.with_columns(pl.col("result_timestamp").apply(lambda s: s.split(" ")[0], return_dtype=pl.Utf8).alias("date"))
    sec = sec.with_columns(pl.col("result_timestamp").apply(lambda s: s.split(" ")[1], return_dtype=pl.Utf8).alias("time"))

    # Split the time column into hour and min columns
    sec = sec.with_columns(pl.col("time").apply(lambda s: s.split(":")[0], return_dtype=pl.Utf8).alias("hour"))
    sec = sec.with_columns(pl.col("time").apply(lambda s: s.split(":")[1], return_dtype=pl.Utf8).alias("min"))
    
    # Convert the date column to datetime format, hour/min to integer
    sec = sec.with_columns(pl.col("hour","min").cast(pl.Int64))
    sec = sec.with_columns(pl.col("date").str.strptime(pl.Datetime, fmt="%d/%m/%Y", strict=False))
    
    
    #Get the average values for laeq, lceq and max value for lamax, lcpeak
    minu = sec.groupby(['date', 'hour', 'min']).agg([pl.col('laeq').mean(), pl.col('lamax').max(), pl.col('lcpeak').max(), pl.col('lceq').mean()])
    minu=minu.sort(['date','hour','min'])

    # Write the result to a Parquet file
    minu.write_parquet(output_path)