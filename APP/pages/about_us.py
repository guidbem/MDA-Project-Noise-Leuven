import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


dash.register_page(__name__, path='/about_us')

# Create the layout of your dashboard
layout = html.Div([
    html.H1('About Us'),
    
    html.Div([
        html.H2('Members:'),
        html.P('This project is done by Ana Sofia Mendes, Federico Soldati, Guilherme Consul Soares de Bem, Ishika Jain, Michelle Hernandez, and Sounak Ghosh.'),
    ])
])
