import os
import pandas as pd
import polars as pl


def datetime_column_splitter(df, column_name):

    if type(df) == pd.DataFrame:
        df[column_name] = pd.to_datetime(df[column_name], format="%d/%m/%Y %H:%M:%S.%f")
        df['date'] = pd.to_datetime(df[column_name].dt.date)
        df['hour'] = df[column_name].dt.hour
        df['minute'] = df[column_name].dt.minute
        df['second'] = df[column_name].dt.second
        df = df.drop(columns=[column_name])

    elif type(df) == pl.DataFrame:
        df = df.with_columns(
        pl.col(column_name).str.strptime(pl.Datetime, "%d/%m/%Y %H:%M:%S.%3f")
        )
        df = df.with_columns(
            pl.col(column_name).dt.date().alias('date'),
            pl.col(column_name).dt.hour().alias('hour').cast(pl.Int32),
            pl.col(column_name).dt.minute().alias('minute').cast(pl.Int32),
            pl.col(column_name).dt.second().alias('second').cast(pl.Int32)
        )
        df = df.drop(columns=[column_name])
    
    return df

def merge_noise_levels(df_ev_mt, n_shifts):

    month_dfs_list = []
    # For loop to go through all the noise levels files
    for lvl_month in os.listdir('noise_levels_parquets'):
        # Reads the noise levels data
        df_noise = pl.read_parquet(f'noise_levels_parquets/{lvl_month}')

        # Select only necessary columns
        df_noise = df_noise.select([
            '#object_id',
            'lamax',
            'laeq',
            'lceq',
            'lcpeak',
            'result_timestamp'])

        # Splits the datetime column in date, hour, minute and second columns
        df_noise = datetime_column_splitter(df_noise, 'result_timestamp')

        # For loop to go through all the shifts
        for shift in range(1, n_shifts+1):
            # Creates the shifted noise level columns
            df_noise = df_noise.with_columns(
                pl.col(f'lamax').shift(-shift).alias(f'lamax_shift_t-_{shift}'),
                pl.col(f'laeq').shift(-shift).alias(f'laeq_shift_t-_{shift}'),
                pl.col(f'lceq').shift(-shift).alias(f'lceq_shift_t-_{shift}'),
                pl.col(f'lcpeak').shift(-shift).alias(f'lcpeak_shift_t-_{shift}')
            )

        # Joins the df_ev_mt and df_noise dataframes on the date, hour, minute, second and #object_id columns
        df_month_tmp = df_ev_mt.join(
            df_noise,
            on=[
                'date',
                'hour',
                'minute',
                'second',
                '#object_id'
            ],
            how='inner'
        )

        month_dfs_list.append(df_month_tmp)

    # Concatenates all the dataframes in the list
    df_ev_mt_lvls = pl.concat(month_dfs_list)

    return df_ev_mt_lvls

