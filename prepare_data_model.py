import polars as pl
import pandas as pd
import numpy as np
from utils import datetime_column_splitter, merge_noise_levels
# Read the noise events data
df_events = pd.read_parquet('noise_events.parquet')

# Drops the "description" and "xx_unit" columns
df_events = df_events.drop(columns=[
    'description',
    'noise_event_laeq_model_id_unit',
    'noise_event_laeq_primary_detected_certainty_unit',
    'noise_event_laeq_primary_detected_class_unit'
    ])

# Drop rows with null values
df_events = df_events.dropna(subset=['noise_event_laeq_primary_detected_class'])

# Converts the result_timestamp column into a datetime column and split it into date and time columns
df_events = datetime_column_splitter(df_events, 'result_timestamp')

# Add a rounded minute column to the nearest ten (needed to join with the meteo data)
df_events['minute_rounded'] = ((df_events['minute']/10).round(0)*10).astype(int)
df_events['hour_rounded'] = np.where(df_events['minute_rounded'] == 60, df_events['hour'] + 1, df_events['hour'])
df_events['hour_rounded'] = np.where(df_events['hour_rounded'] == 24, 0, df_events['hour_rounded'])
df_events['minute_rounded'] = np.where(df_events['minute_rounded'] == 60, 0, df_events['minute_rounded'])

# Converts the events dataframe into a polars dataframe
df_events = pl.from_pandas(df_events)

# Removes the time from the date column (happens after converting to polars)
df_events = df_events.with_columns(
    pl.col('date').dt.date())

# Reads the meteorological data
df_meteo = pl.read_parquet('meteo_data.parquet')

# Select only necessary columns in the meteo dataframe
df_meteo = df_meteo.select([
    'LC_RAININ',
    'LC_WINDSPEED',
    'Date',
    'Hour',
    'Minute',
    'LC_RAD60',
    'LC_TEMP_QCL3'
    ])

# Converts the Date column in a datetime column
df_meteo = df_meteo.with_columns(
    pl.col('Date').str.strptime(pl.Datetime, '%Y-%m-%d').alias('date').dt.date())
df_meteo = df_meteo.drop('Date')

# Converts the Hour and Minute columns in i32 columns
df_meteo = df_meteo.with_columns(
    pl.col('Hour').cast(pl.Int32),
    pl.col('Minute').cast(pl.Int32)
    )

# Groups the meteo data by date, hour and minute and takes the mean of the other columns
df_meteo = df_meteo.groupby(['date', 'Hour', 'Minute']).mean()

# Joins the df_events and df_meteo dataframes on the date, hour and minute columns
df_ev_mt = df_events.join(
    df_meteo,
    left_on=['date', 'hour', 'minute_rounded'],
    right_on=['date', 'Hour', 'Minute'],
    how='left')

df_ev_mt = df_ev_mt.drop(columns=['minute_rounded', 'hour_rounded'])

# Joins the events and meteo dataframe with the noise levels dataframes
df_ev_mt_lvls = merge_noise_levels(df_ev_mt, n_shifts=5)

# Saves the dataframe as a parquet file
df_ev_mt_lvls.write_parquet('pred_model_data_full.parquet')
