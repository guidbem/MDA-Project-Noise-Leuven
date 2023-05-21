import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dash_table
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/model')


data = {
    'Accuracy': [0],
    'Precision': [0],
    'Recall': [0],
    'F1-Score': [0]
}
df = pd.DataFrame(data)


# Define the layout
layout = html.Div([

    html.H1('Model - To do:'),
    
    html.Div([
        html.P('Confusion Matrix, Classification Table, ROC curve, Insert .csv file')
    ]),
    #--------- Add other necessary things here ---------#
    html.Div(
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),
        style={'width': '300px'}
    ),

    # For the new upload
    dcc.Upload(dbc.Button('Upload File', id="upload-button", n_clicks=0, 
                          style={"margin-right": "25px","margin-top": "0px","zIndex": "0"},outline=False, color="danger", className="me-1"))
])


# For the new CSV that will be uploaded

@callback(Output('output-data-upload', 'children'),
              [Input('upload-button', 'n_clicks')],
              [State('upload-data', 'contents'),
               State('upload-data', 'filename')])
def update_output(n_clicks, contents, filename):
    if n_clicks > 0:
        if contents is not None:
            df = pd.read_csv(contents)
            # Perform your visualizations or data processing here
            # Return the result, such as a graph or a table
            return html.Div([
                html.H5(f'Uploaded File: {filename}'),
                html.Hr(),
                html.Div(df.head())
            ])
    return html.Div()