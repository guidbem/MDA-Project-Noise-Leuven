import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html, dcc

dash.register_page(__name__, path='/about_us')

# Define the layout

layout = html.Div([
    html.H1('About Us'),
    
    html.Div([
        html.H2('Members:'),
        html.P('This project is done by Ana Sofia Mendes, Federico Soldati, Guilherme Consul Soares de Bem, Ishika Jain, Michelle Hernandez, and Sounak Ghosh.'),
    ])
])
