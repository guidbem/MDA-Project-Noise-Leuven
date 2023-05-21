import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/analysis-2')

layout=html.Div([
    html.H1('Analysis 2')
])