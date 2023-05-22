import os
import pandas as pd
import polars as pl
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction import FeatureHasher
from sklearn.decomposition import PCA
from category_encoders.binary import BinaryEncoder
import numpy as np
import pandas as pd


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

class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_new = X.copy()
        X_new.drop(columns=self.columns_to_drop, inplace=True)
        return X_new
    
class DayPeriodHandler(BaseEstimator, TransformerMixin):
    def __init__(self, hour_column='hour', day_period_column='day_period'):
        self.hour_column = hour_column
        self.day_period_column = day_period_column

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_new = X.copy()

        bins = [-1,6,12,18,23]

        labels = ['dawn', 'morning', 'afternoon', 'night']

        X_new[self.day_period_column] = pd.cut(
            X_new[self.hour_column], 
            bins=bins, 
            labels=labels).astype(str)

        return X_new


class MonthHandler(BaseEstimator, TransformerMixin):
    """
    Transforms a date column into a month column.
    The final column can be either strings of the month numbers (strategy 'month') 
    or strings containing the seasons (strategy 'season').
    """
    def __init__(self, date_column='date', month_column='month', strategy='month'):
        self.date_column = date_column
        self.month_column = month_column
        self.strategy = strategy

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_new = X.copy()

        X_new[self.date_column] = pd.to_datetime(X_new[self.date_column])

        if self.strategy == 'month':
            X_new[self.month_column] = X_new[self.date_column].dt.month.astype(str)
        
        elif self.strategy == 'season':
            bins = [0,2,5,8,12]

            labels = ['winter', 'spring', 'summer', 'autumn']

            X_new[self.month_column] = pd.cut(
                X_new[self.date_column].dt.month, 
                bins=bins, 
                labels=labels).astype(str)
            
            X_new[self.month_column] = np.where(
                X_new[self.date_column].dt.month == 12,
                'winter', 
                X_new[self.month_column])
        
        return X_new


class DayoftheWeekHandler(BaseEstimator, TransformerMixin):
    """
    Transforms a date column into a day of the week column.
    The final column can be either strings of the weekday numbers (strategy 'full') 
    or strings containing if it is a weekday or weekend (strategy 'weekday_cats').
    """
    def __init__(self, date_column='date', weekday_column='weekday', strategy='full'):
        self.date_column = date_column
        self.weekday_column = weekday_column
        self.strategy = strategy

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_new = X.copy()

        if self.strategy == 'full':
            X_new[self.weekday_column] = X_new[self.date_column].dt.weekday.astype(str)
        
        elif self.strategy == 'weekend':
            X_new[self.weekday_column] = np.where(
                X_new[self.date_column].dt.weekday <= 3,
                'weekday', 
                'weekend')
        
        return X_new

        
class CustomEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns, strategy='one_hot'):
        self.columns = columns
        self.strategy = strategy
        
    def fit(self, X, y=None):
        for col in self.columns:
            if X[col].dtype != 'object':
                X[col] = X[col].astype(str)

        if self.strategy == 'one_hot':
            cats_to_remove = [
                X[i].value_counts().index[-1] 
                for i in self.columns
                ]
            self.encoder = OneHotEncoder(drop=cats_to_remove)
            self.encoder.fit(X[self.columns])
        
        elif self.strategy == 'binary':
            self.encoder = BinaryEncoder(cols=self.columns)
            self.encoder.fit(X)
        
        return self
    
    def transform(self, X, y=None):
        X_new = X.copy()

        if self.strategy == 'one_hot':
            feature_names = self.encoder.get_feature_names_out(self.columns)
            X_new[feature_names] = self.encoder.transform(X_new[self.columns]).toarray()
            X_new.drop(columns=self.columns, inplace=True)
        
        elif self.strategy == 'binary':
            X_new = self.encoder.transform(X_new)
        
        return X_new

class PCATransformer(BaseEstimator, TransformerMixin):
    def __init__(self, n_components=2, columns=None):
        self.n_components = n_components
        self.columns = columns
        
    def fit(self, X, y=None):
        if self.columns is None:
            self.columns = list(X.columns)
        
        self.pca = PCA(n_components=self.n_components)
        self.pca.fit(X[self.columns])
        self.comps_cols = ['noise_lvl_comp_'+str(i) for i in range(1,self.n_components+1)]

        return self
    
    def transform(self, X, y=None):
        X_new = X.copy()
        X_new[self.comps_cols] = self.pca.transform(X_new[self.columns])
        X_new.drop(columns=self.columns, inplace=True)
        return X_new



