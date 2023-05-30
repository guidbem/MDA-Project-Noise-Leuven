import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/analysis-2')

layout = html.Div([
    html.H1('Analysis 2: Can meteo data be used to predict noise levels?'),
    html.Div(
    children=[
        html.P("In order to see whether the meteo data can be used to predict noise levels or not, we can perform granger causality test. Granger causality is an econometric test used to verify the usefulness of one variable to forecast another."
               "We have the crowdsourced data of the year 2022 from 100 low-cost weather stations in Leuven, which contains observations of 13 weather-related variables with a sampling period of 10 minutes. "
               "Principal Component Analysis (PCA) is a dimensionality reduction technique that can be applied to the weather data to extract meaningful features and reduce the dimensionality of our dataset."
               " PCA can help us visualize high-dimensional weather data in a lower-dimensional space. By projecting the data onto a smaller number of principal components, we can then use those components for the granger causality test instead of testing for all the variables separately."
               "So we conduct PCA on the meteo data, and extract the first two principal components that contribute the most to the overall variance in the data."
               "The following is the biplot where each variable is represented as a vector. The position and orientation of the vectors indicate the contribution of each variable to the principal components"),
        
        

    ]),
    
    html.Div(html.Img(src="assets/Meteo_PCA.png", style={'display': 'block', 'margin': 'auto'})),
    html.Div(
    children=[
        html.P("The plot indicates that the variables related to temperature and radiation are explained by the first principal component"
               "Whereas, the variables related to raining, wind speed and direction are better explained by the second component."
                "The variable Humidity is contributing to both the principal components."),
        
        

    ]),
    html.Div(
    children=[
        html.P("we plot the components to check whether they are stationary: "
               "The time-series does not look stationary, thus we do differencing. Differencing can help achieve stationarity by removing trends and making the series more stable over time."
               "By subtracting the previous observation from the current observation, the resulting differenced series represents the change or deviation from the previous value. This helps in focusing on the fluctuations or irregularities in the data."
               "We can also expect some seasonality as the first component is explained by the variables such as temperature, which follow a daily trend, as one can expect the temperature in the morning to be correlated to the temperature of previous morning."
               "Therefore we difference the series at 144 lags, in order to remove the daily trend"),
        
        

    ]),
    html.Div(
    children=[
        html.P("Since noise levels data was available in seconds, we transformed it to match the sampling period of meteo data by taking the mean over 10 minutes of the values of 'laeq' and 'lceq' whereas maximum values of 'lamax' and 'lcpeak'."
               "To check for the requirement of stationarity, we plot the ACF (Autocorrelation Function) plot which is a graphical tool used in time series analysis to visualize the correlation between a time series and its lagged values. "
               "A time series can be assumed to be stationary if there are no significant autocorrelations between observations at different time points."
               "We can clearly see high autocorrelations, and some seasonality in the left plot, we therefore compute the differences between consecutive observations to remove trends, seasonality, or other non-stationary components present in the data"
               "The middle plot represents the acf plot after differencing, we can still see some small peaks at every (approx 144 lags) few lags, thus implying some seasonality around lag 144, which is due to the daily pattern which is repeated every 24 hrs. So we do differencing again with 144 lags in order to eliminate the seasonal pattern."
               "We obtain the figure in the right as the acf plot after differencing twice, which seems to be stationary. We also performed ADFuller test to verify the stationary."),
        
        

    ]),
    html.Div([
        html.Img(src="assets/acf_minutes_noise.png", style={'width': '33%'}),
        html.Img(src="assets/diff1_laeq.png", style={'width': '33%'}),
                html.Img(src="assets/diff1_144.png", style={'width': '33%'}),
    ], style={'display': 'flex'}),
    html.Div(
    children=[
        html.P("Now that the assumption of stationarity is accomplished, we can use the differenced time series to test whether the meteo data has an explanatory power in predicting the noise levels."
               "We perform the granger causality test of both the principal components on 'laeq' and 'lceq', and find the following results:"),
    ]),
    html.Div(
    children=[
        html.P("We can see that all the p-values are above 0.05, thus we do not reject the null hypothesis of no granger causality. Therefore meteo data do not have a significant explanatory power in predicting laeq or lceq."
               "Even though there exist a correlation between the components and the noise levels, we did not find any granger causality, it implies that the correlation could be because of the time. To explain it in a better way"
               ", the temperature during the night and early morning are usually lower than the day-time, similarly the noise level is expected to be higher during day-time, which might cause both the time series to have a similar trend but it wont imply one of them is causing other, or vice-versa."),
    ])
])