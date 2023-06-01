import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/analysis-2')

card_main = dbc.Card(
    [        dbc.CardBody(
            [
                html.H2("Principal Component Analysis on the Meteo Data", className="card-title",style={"color": "#dc3545", "paddingTop": "50px", "textAlign": "left","fontSize": "32px"}),
                html.H3("Findings:", className="card-subtitle",style={"paddingTop": "25px", "textAlign": "left","fontSize": "28px"}),
                html.Ul(
                    children=[
                        html.Li("The variables related to temperature and radiation are highly influencing the first principal component, as their projection on PC1 is high."),
                        html.Li("The variables related to raining and wind have higher projections on PC2, thereby having a higher contribution in explaining the variance of PC2."),
                        html.Li("Humidity has high projections on both PC1 and PC2, thus it is affecting both the components."),
                        html.Li("The length of the vector of windspeed is very short, which means its variance is not being explained by either of the principal components.")
                    ], className="card-text",
                      style={
                        "paddingTop": "20px",  # Add spacing at the top
                        "paddingBottom": "50px",  # Add spacing at the bottom
                        "textAlign": "left",
                        "margin": "0",
                        "fontSize": "18px"  # Increase font size
                    }
                ),
                
               
            ]
        ),
    ],
    color="light",
    inverse=False,  # change color of text (black or white)
      outline=False,
      style={'height': '500px'}
)

card_pic = dbc.Card(
    [
        dbc.CardImg(src="assets/Meteo_PCA.png",top=True, bottom=False, className="mx-auto", style={'height': '400px'}),
        dbc.CardBody([
            
            html.H3("PCA Biplot",className="text-center",style={"color": "#dc3545","fontSize": "28px"})
        ])
        
    ],
     outline=False,
     style={'height': '500px'}
)
card_granger_main = dbc.Card(
    [        dbc.CardBody(
            [
                html.H2("Conclusions:", className="card-title",style={"color": "#dc3545", "paddingTop": "50px", "textAlign": "center","fontSize": "32px"}),
                html.H3("The Granger causality test is a statistical hypothesis test for determining whether one time series is useful in forecasting another.", className="card-subtitle",style={"paddingTop": "25px", "textAlign": "left","fontSize": "28px"}),
                html.Ul(
                    children=[
                        html.Li("All the p-values are above 0.05, thus we cannot reject the null hypothesis of no granger causality. Therefore, the meteo data cannot be used to predict the noise levels."),
                        html.Li("The correlation between the noise levels and the principal components could be merely due to the time, or in other words both the weather data as well as noise data follow the same daily trend which results in correlation.")
                         ], className="card-text",
                      style={
                        "paddingTop": "20px",  # Add spacing at the top
                        "paddingBottom": "50px",  # Add spacing at the bottom
                        "textAlign": "left",
                        "margin": "0",
                        "fontSize": "18px"  # Increase font size
                    }
                ),
                
               
            ]
        ),
    ],
    color="light",
    inverse=False,  # change color of text (black or white)
      outline=False,
      style={'height': '500px'}
)
card_granger = dbc.Card(
    [
        dbc.CardImg(src="assets/granger.png",top=True, bottom=False, className="mx-auto", style={'height': '400px'}),
        dbc.CardBody([
            
            html.H3("Visualizing the time series",className="text-center",style={"color": "#dc3545","fontSize": "28px"})
        ])
        
    ],
     outline=False,
     style={'height': '500px'}
)

card_acf = dbc.Card(
    [        dbc.CardBody(
            [
                html.H2("Stationarity", className="card-title",style={"color": "#dc3545", "paddingTop": "50px", "textAlign": "left","fontSize": "32px"}),
                
                
                
               
            ]
        ),
    ],
    color="light",
    inverse=False,  # change color of text (black or white)
      outline=False,
      style={'height': '600px'}
)

card_acf1 = dbc.Card(
    [
        dbc.CardImg(src="assets/acf_minutes_noise.png",top=True, bottom=False, className="mx-auto", style={'height': '400px'}),
        dbc.CardBody([
            
            html.H3("1. ACF before differencing",className="text-center",style={"color": "#dc3545","fontSize": "28px"}),
            html.H3("Findings:", className="card-subtitle",style={"paddingTop": "25px", "textAlign": "left","fontSize": "24px"}),
            html.Ul(
                    children=[
                        html.Li("The autocorrelation plots of the noise levels data shows high correlations at almost all lags, and do not seem to converge to zero, thereby implying non-stationarity."),
                        html.Li("We can also notice some seasonality as the pattern in the acf plots repeats after every few lags.")
                        
                    ], className="card-text",
                      style={
                        "paddingTop": "20px",  # Add spacing at the top
                        "paddingBottom": "50px", # Add spacing at the bottom
                        "textAlign": "left",
                        "margin": "0",
                        "fontSize": "18px"  # Increase font size
                    }
                )
        ])
        
    ],
     outline=False,
     style={'height': '650px'}
)
card_acf2 = dbc.Card(
    [
        dbc.CardImg(src="assets/diff1_laeq.png",top=True, bottom=False, className="mx-auto", style={'height': '400px'}),
        dbc.CardBody([
            
            html.H3("2. ACF after differencing at lag 1",className="text-center",style={"color": "#dc3545","fontSize": "28px"}),
            html.H3("Findings:", className="card-subtitle",style={"paddingTop": "25px", "textAlign": "left","fontSize": "24px"}),
                html.Ul(
                    children=[
                        html.Li("The autocorrelations are reduced to a large extent."),
                        html.Li("We can still notice some small peaks (approx thrice in every 500 lags), these peaks could be because of the daily pattern in noise levels(6(1hr=6 lags)*24(hrs in a day)=144 lags)."),
                         ], className="card-text",
                      style={
                        "paddingTop": "20px",  # Add spacing at the top
                         "paddingBottom": "50px", # Add spacing at the bottom
                        "textAlign": "left",
                        "margin": "0",
                        "fontSize": "18px"  # Increase font size
                    }
                )
        ])
        
    ],
     outline=False,
     style={'height': '650px'}
)
card_acf3 = dbc.Card(
    [
        dbc.CardImg(src="assets/diff1_144.png",top=True, bottom=False, className="mx-auto", style={'height': '400px'}),
        dbc.CardBody([
            
            html.H3("3. ACF after differencing at lag 144",className="text-center",style={"color": "#dc3545","fontSize": "28px"}),
            html.H3("Findings:", className="card-subtitle",style={"paddingTop": "25px", "textAlign": "left","fontSize": "24px"}),
                html.Ul(
                    children=[
                        html.Li("The time series appears stationary now."),
                        html.Li("Our observation was seconded by the results of ADF test, as the p-value is 0 for the double-differenced series, implying stationarity.")
                    ], className="card-text",
                      style={
                        "paddingTop": "20px",  # Add spacing at the top
                        "paddingBottom": "50px",  # Add spacing at the bottom
                        "textAlign": "left",
                        "margin": "0",
                        "fontSize": "18px"  # Increase font size
                    }
                )
        ])
        
    ],
     outline=False,
     style={'height': '650px'}
)



box_style_granger = {
    'height': '250px',
    'width': '300px',
    'background-color': 'olive',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '150px',
    'left': '15px',
    'clip-path': 'polygon(0 0, 100% 0%, 100% 92%, 85% 100%, 0% 100%)',
    '-webkit-clip-path': 'polygon(0 0, 100% 0%, 100% 92%, 85% 100%, 0% 100%)',
    'font-family':'Tiffany'
}

box_style_pca_findings = {
    'height':'250px',
    'width':'650px',
    'background-color': 'mediumturquoise',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '500px',
    'left': '15px'
}

box_style_stationary = {
    'height':'250px',
    'width':'1000px',
    'background-color': 'orangered',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '800px',
    'left': '15px'
}

box_style_stationary_findings = {
    'height':'450px',
    'background-color': 'mediumturquoise',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '1500px',
    'left': '15px'
}

layout = html.Div([
        html.H1('Can meteo data be used to predict noise levels?' ,style={"paddingLeft": "20px"}),

    dbc.Row(
    [
        dbc.Col(card_main, width=6),
        dbc.Col(card_pic, width=4),
    ],
    className="my-4",
    justify="center",
),
dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                html.H2("Differencing and removing seasonal trends to obtain stationary noise levels:", className="card-title",style={"color": "#dc3545", "paddingTop": "50px", "textAlign": "center","fontSize": "32px"}),
                html.P("A stationary time series is one whose properties do not depend on the time at which the series is observed. Thus, time series with trends, or with seasonality, are not stationary — the trend and seasonality will affect the value of the time series at different times."), 
                dbc.Row(
    [
        
        dbc.Col(card_acf1, width=4),
        
        dbc.Col(card_acf2, width=4),
        dbc.Col(card_acf3, width=4)
    ],
    className="my-4",
    justify="center",
)
                ]
            ),
            className="my-4",
      color="light",
    inverse=False,  # change color of text (black or white)
      outline=False,
      style={'height': '950px'}  )
    ],
    fluid=True
    
),
 dbc.Row(
    [
        dbc.Col(card_granger, width=4),
        dbc.Col(card_granger_main, width=6),
    ],
    className="my-4",
    justify="center",
),
    # Granger Definition

        #html.Div(
         #   children= [
          #      html.H3("Granger Causality", style={'font-weight': 'bold'}),
           #     html.P(" The Granger causality test is a statistical hypothesis test for determining whether one time series is useful in forecasting another, first proposed in 1969. Granger causality is an econometric test used to verify the usefulness of one variable to forecast another."),
            #], style= box_style_granger 
        #),

# PCA plot
       # html.Div(
        #    children=[
         #       html.Img(
          #          src="assets/Meteo_PCA.png",
           #         style={
            #            'display': 'block',
             #           'height': '500px',
              ##         'padding': '10px',
                #        'border-radius': '5px',
                 #       'margin-bottom': '10px',
                  #      'position': 'absolute',
                   #     'top': '150px',
                    #    'right': '15px',
                     #   'background-color': 'purple'
     #               }
      #          )
       #     ]
        #),



    # PCA Findings text

    #    html.Div(
     #       children=[
      #          html.H3("Findings"),
       #         html.Ul(
        #            children=[
         #               html.Li("The variables related to temperature and radiation are highly influencing the first principal component, as their projection on PC1 is high."),
          #              html.Li("The variables related to raining and wind have higher projections on PC2, thereby having a higher contribution in explaining the variance of PC2."),
           #             html.Li("Humidity has high projections on both PC1 and PC2, thus it is affecting both the components."),
            #            html.Li("The length of the vector of windspeed is very short, which means its variance is not being explained by either of the principal components.")
             #       ]
              #  )
      #      ],
       #     style=box_style_pca_findings
        #),


    # Stationary time series defintion

   #     html.Div(
    #    children=[
     #       html.H3("Stationary Time Series", style={"text-align": "center"}),
      #      html.P("A stationary time series is one whose properties do not depend on the time at which the series is observed. Thus, time series with trends, or with seasonality, are not stationary — the trend and seasonality will affect the value of the time series at different times. On the other hand, a white noise series is stationary — it does not matter when you observe it, it should look much the same at any point in time. Some cases can be confusing — a time series with cyclic behaviour (but with no trend or seasonality) is stationary. This is because the cycles are not of a fixed length, so before we observe the series we cannot be sure where the peaks and troughs of the cycles will be. In general, a stationary time series will have no predictable patterns in the long-term. Time plots will show the series to be roughly horizontal (although some cyclic behaviour is possible), with constant variance."),
       # ], style=box_style_stationary
        #),

    # ACF Plots

 #   html.Div([
  #       html.Figure(
   #                 children=[
    ###              html.Img(src="assets/diff1_144.png", style={'width': '33%'}), html.Figcaption('ACF After Differencing twice')
       # ], style={'display': 'flex',
       # 'width':'1000px', 'padding': '10px', 'border-radius': '5px', 'margin-bottom': '10px', 'position': 'absolute', 'top': '1100px', 'left': '15px'})
   # ]),

    # Findings From the Stationary
    #    html.Div(
     #   children=[
      #      html.H3("Findings"),
       #     html.Ul(
        #    children=[
         #       html.H3("Findings"),
          #      html.Ul(
           #         children=[
            #            html.Li("The autocorrelation plots of the noise levels data shows high correlations at almost all lags, and do not seem to converge to zero, thereby implying non-stationarity."),
             #           html.Li("We can also notice some seasonality as the pattern in the acf plots repeats after every few lags."),
              #          html.Li("The autocorrelations are reduced to a large extent."),
               #         html.Li("We can still notice some small peaks (approx thrice in every 500 lags), these peaks could be because of the daily pattern in noise levels(6(1hr=6 lags)*24(hrs in a day)=144 lags)."),
                #        html.Li("The time series appears stationary now."),
                 #       html.Li("Our observation was seconded by the results of ADF test, as the p-value is 0 for the double-differenced series, implying stationarity.")
                  #  ]
               # )
           # ],                
        #        style=box_style_stationary_findings
       # )
  #  ])
])