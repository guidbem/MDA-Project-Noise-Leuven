import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from statsmodels.graphics.tsaplots import plot_acf
import pyarrow.parquet as pq
import polars as pl
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller

def avg_Meteo(parquet_file_path: str, output_path: str) :
    #Converting the date column to pandas datetime format and taking the average for all the 100 meters
    meteo=pd.read_parquet(parquet_file_path)
    meteo['DATEUTC'] = pd.to_datetime(meteo['DATEUTC'])
    meteo = meteo.set_index('DATEUTC')
    # Dropping non-numerical columns
    meteo.drop(columns=['ID', 'Date'], inplace=True)
    meteo_avg=meteo.groupby(level=0).mean()
    meteo_avg=pd.DataFrame(meteo_avg)
    meteo_avg.to_parquet(output_path)

def PCA_meteo(parquet_file_path: str, output_path: str):
    # Extract numerical data
    meteo=pd.read_parquet(parquet_file_path)
    numerical_data = meteo.drop(columns=["Year", "Month",
                                            "Day", "Hour", "Minute","LC_n"])
    numerical_data=numerical_data.dropna()
    # Standardize the data
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(numerical_data)
    std_data= pd.DataFrame(standardized_data)
    standardized = pd.DataFrame(scaler.fit_transform(numerical_data), columns=numerical_data.columns, index=numerical_data.index)
    # Select the number of components to keep based on the plot
    n_components = 2
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(standardized_data)
    pca_data_i=pd.DataFrame(pca_data, index=standardized.index)
    # Get the top principal components
    top_components = pca_data[:, :n_components]
    # Get the explained variance ratio
    explained_variance_ratio = pca.explained_variance_ratio_
    # Get the loadings (correlation between the original features and the principal components)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    # Plot the biplot
    fig, ax = plt.subplots()
    for i, feature in enumerate(std_data.columns):
        ax.arrow(0, 0, loadings[i, 0], loadings[i, 1], color='r', alpha=0.8)
        ax.text(loadings[i, 0]*1.15, loadings[i, 1]*1.15, numerical_data.columns[feature], color='g', ha='center', va='center')
    ax.set_xlabel('PC1 ({:.2f}%)'.format(explained_variance_ratio[0]*100))
    ax.set_ylabel('PC2 ({:.2f}%)'.format(explained_variance_ratio[1]*100))
    ax.set_title('Biplot for PCA')
    plt.show()
    pca_comp = pd.DataFrame(top_components, index=standardized.index, columns=['PC1','PC2'])
    pca_comp.to_parquet(output_path)
def differencing(parquet_file_path:str, varname: str, st_varname:str) :
    df=pd.read_parquet(parquet_file_path)
    df[st_varname]=df[varname].diff(1)
    df.dropna(inplace=True)
    df.to_parquet(parquet_file_path)
def differencing_144(parquet_file_path:str, varname: str, st_varname:str) :
    df=pd.read_parquet(parquet_file_path)
    df[st_varname]=df[varname].diff(144)
    df.dropna(inplace=True)
    df.to_parquet(parquet_file_path)
def test_stationarity(parquet_file_path:str, varname:str):
    df=pd.read_parquet(parquet_file_path)
    result = adfuller(df[varname])
    # Print the test statistic and p-value
    print(f"ADF statistic: {result[0]}")
    print(f"p-value: {result[1]}")
def noise_resampling(parquet_file_path:str, output_file_path:str):
    noise = pd.read_parquet(parquet_file_path)
    sorted_noise=noise.sort_values(by=['date','hour','min'])
    sorted_noise['timestamp'] = pd.to_datetime(sorted_noise['date']) + pd.to_timedelta(sorted_noise['hour'], unit='h') + pd.to_timedelta(sorted_noise['min'], unit='m')
    sorted_noise = sorted_noise.set_index('timestamp')
    df_mean = sorted_noise.resample('10T').mean()
    df_max = sorted_noise.resample('10T').max()
    noise_resampled = pd.concat([df_mean['laeq'], df_mean['lceq'], df_max['lcpeak'],df_max['lamax']], axis=1)
    noise_resampled1=pd.DataFrame(noise_resampled)
    noise_resampled=noise_resampled1.dropna()
    noise_resampled.to_parquet(output_file_path)
def merge_noise_meteo(noise_file_path:str ,meteo_file_path:str , pca_file_path:str,output_file_path: str) :
    noise_resampled=pd.read_parquet(noise_file_path)
    meteo=pd.read_parquet(meteo_file_path)
    pca_comp=pd.read_parquet(pca_file_path)
    merged=pd.merge(noise_resampled, meteo, left_index=True, right_index=True)
    granger=pd.merge(merged, pca_comp, left_index=True, right_index=True)
    granger.to_parquet(output_file_path)
def test_granger_causality(parquet_file_path:str, var1:str, var2:str):
    granger=pd.read_parquet(parquet_file_path)
    data = granger[[var1, var2]]
    # Perform Granger causality test
    max_lag = 1
    results = grangercausalitytests(data, max_lag)
    # Extract p-values or other statistics from the results
    for lag in range(1, max_lag+1):
        p_value = results[lag][0]['ssr_ftest'][1]
        print(f"Lag {lag}: p-value = {p_value}")


    

