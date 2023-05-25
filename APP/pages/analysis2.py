import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/analysis-2')

layout = html.Div([
    html.H1('Analysis 2'),
    html.Div([
        html.Img(src="assets/acf_minutes_noise.png", style={'width': '33%'}),
        html.Img(src="assets/diff1_laeq.png", style={'width': '33%'}),
                html.Img(src="assets/diff1_144.png", style={'width': '33%'}),
    ], style={'display': 'flex'}),
    html.Div(html.Img(src="assets/Meteo_PCA.png", style={'display': 'block', 'margin': 'auto'}))
])