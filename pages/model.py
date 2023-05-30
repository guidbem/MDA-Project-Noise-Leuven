import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dash_table
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/model')


classification_report_data = {
    'Class': ['Human voice - Shouting', 'Human voice - Singing', 'Other', 'Transport road - Passenger car', 'Transport road - Siren', ' ', 'accuracy', 'macro avg', 'weighted avg'],
    'Precision': [0.77, 0.72, 1.00, 0.97, 0.80, ' ', '-', 0.85, 0.95],
    'Recall': [0.78, 0.44, 0.99, 0.98, 0.67, ' ', '-', 0.77, 0.95],
    'F1-Score': [0.77, 0.54, 1.00, 0.97, 0.73, ' ', 0.95, 0.80, 0.95],
    'Support': [1671, 352, 6224, 14301, 622, ' ', 23170, 23170, 23170]
}
classification_report_df = pd.DataFrame(classification_report_data)

fig = '/assets/confusion_matrix.png'
balanced_accuracy = 77.2

# Define the layout
layout = html.Div([

    #html.H1('Model - To do:'),
    
    #html.Div([
    #    html.P('Confusion Matrix, Classification Table, ROC curve, Insert .csv file')
    #]),
    #--------- Add other necessary things here ---------#


    dbc.Row([
        dbc.Col([
            html.H3('Classification Report', style={'margin-left':'50px'}),
            dbc.Table(
                id='classification-report-table',
                bordered=True,
                striped=True,
                hover=True,
                responsive=True,
                style={'margin-left':'50px','width': '690px'},
                children=[
                    html.Thead([
                        html.Tr([
                            html.Th('Class'),
                            html.Th('Precision'),
                            html.Th('Recall'),
                            html.Th('F1-Score'),
                            html.Th('Support')
                        ])
                    ]),
                    html.Tbody([
                        html.Tr([
                            html.Td(classification_report_df.iloc[i]['Class']),
                            html.Td(classification_report_df.iloc[i]['Precision']),
                            html.Td(classification_report_df.iloc[i]['Recall']),
                            html.Td(classification_report_df.iloc[i]['F1-Score']),
                            html.Td(classification_report_df.iloc[i]['Support'])
                        ]) for i in range(len(classification_report_df))
                    ])
                ]
            ),
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Balanced accuracy", className="card-title"),
                        html.H3(f"{balanced_accuracy:.2f} %", className="card-text"),
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(176, 224, 230, 0.7)', "margin": "auto", "maxWidth": "fit-content", "padding": "10px"})
            ]),
        ], width=6), 
        dbc.Col([
        html.H3('Confusion Matrix', style={'margin-left':'70px'}),
        html.Img(src=fig, style={'width': '600px', 'margin-left':'70px', 'border': '1px solid black'})
        ], width=6)
    ]),

# For the new upload
    html.H2('Predictions', style={'margin-top':'50px', 'margin-right':'100px'}),

    dcc.Upload(
        dbc.Button('Upload File', id="upload-button", n_clicks=0, 
                          style={"margin-right": "25px","margin-top": "0px","zIndex": "0"},outline=False, color="info", className="me-1")),

    html.Div(id='output-data-upload'),
    html.Div(id='prediction-results')
])


# Define the callback function
@callback(
    [Output('output-data-upload', 'children'),
     Output('prediction-results', 'children')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is not None:
        df = pd.read_csv(contents)
        # Perform your visualizations or data processing here
        # Return the result, such as a graph or a table
        return html.Div([
            html.H5(f'Uploaded File: {filename}'),
            html.Hr(),
            html.Div(df.head())
        ]), None
    return html.Div(), None