import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/model')


layout = html.Div([
    html.H1('Model - To do:'),
    
    html.Div([
        html.P('Confusion Matrix, Classification Table, ROC curve, Insert .csv file')
    ])
])