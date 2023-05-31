import pandas as pd
import pickle
import plotly.graph_objects as go
import dash
from dash import dash_table
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask, send_file
import io
from urllib.parse import quote
import base64

#from sklearn.pipeline import Pipeline, make_pipeline
#from sklearn.model_selection import train_test_split, KFold, cross_val_score, StratifiedKFold, GridSearchCV, RandomizedSearchCV
#from lightgbm import LGBMClassifier
#from sklearn.preprocessing import FunctionTransformer
#from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, classification_report, balanced_accuracy_score
#import pandas as pd
#import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
#from pprint import pprint
#from skopt import BayesSearchCV
#from skopt.space import Real, Integer
#from utils.model_datatransforms import *



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

label = {
    'Number': [0, 1, 2, 3, 4],
    'String': ['Human voice - Shouting', 'Human voice - Singing', 'Other', 'Transport road - Passenger car', 'Transport road - Siren']
}
df_label = pd.DataFrame(label)


# Define the layout
layout = html.Div([

    #html.H1('Model - To do:'),
    
    #html.Div([
    #    html.P('Confusion Matrix, Classification Table, ROC curve, Insert .csv file')
    #]),
    #--------- Add other necessary things here ---------#


    dbc.Row([
        dbc.Col([
            html.H3('Classification Report', style={'margin-left':'50px', 'margin-top':'10px'}),
            dbc.Table(
                id='classification-report-table',
                bordered=True,
                striped=True,
                hover=True,
                responsive=True,
                style={'margin-left':'50px',
                       'width': '690px',
                       'margin-top':'10px',
                       'font-size': '14px',
                        'text-align': 'center',
                        'border-collapse': 'collapse',
                        'border-spacing': '0'},
                children=[
                    html.Thead([
                        html.Tr([
                            html.Th('Class'),
                            html.Th('Precision'),
                            html.Th('Recall'),
                            html.Th('F1-Score'),
                            html.Th('Support')
                        ])
                    ], style={
                    'background-color': 'rgba(0, 0, 0, 0.1)',
                    'font-weight': 'bold',
                    }),
                    html.Tbody([
                        html.Tr([
                            html.Td(classification_report_df.iloc[i]['Class']),
                            html.Td(classification_report_df.iloc[i]['Precision']),
                            html.Td(classification_report_df.iloc[i]['Recall']),
                            html.Td(classification_report_df.iloc[i]['F1-Score']),
                            html.Td(classification_report_df.iloc[i]['Support'])
                        ],
                        style={
                        'background-color': 'rgba(255, 255, 255, 1)' if i % 2 == 0 else 'rgba(0, 0, 0, 0.05)'}
                    ) for i in range(len(classification_report_df))
                    ])
                ]
            ),
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Balanced accuracy", className="card-title"),
                        html.H3(f"{balanced_accuracy:.2f} %", className="card-text"),
                    ])
                ], className="mb-4", style={'backgroundColor':'rgba(255, 0, 0, 0.4)', "margin": "auto", "maxWidth": "fit-content", "padding": "10px"})
            ]),
        ], width=6), 
        dbc.Col([
        html.H3('Confusion Matrix', style={'margin-left':'70px', 'margin-top':'10px'}),
        html.Img(src=fig, style={'width': '600px', 'margin-left':'70px', 'border': '1px solid black', 'margin-top':'10px'})
        ], width=6)
    ], style={'background-color': '#F5F5F5'}),

    html.Div(children=[
        # Horizontal line
        html.Div( style={"position": "absolute", "left": "0", "top": "68px", "width": "100%", "height": "2px", "backgroundColor": "lightgray", "zIndex": "0"}),
       ]),

    # For the new upload
    html.H2('Predictions', style={'margin-top':'50px', 'margin-left':'20px'}),

    html.P('Please insert a .csv file to add the labels', style={'margin-left':'20px'}),

    html.Div([
        html.Div([
            dcc.Upload(
                id="upload-data",
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '300px',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin-left': '20px',
                    'display': 'inline-block'
                },
                multiple=False
            ),
        ], style={'display': 'inline-block'}),
        html.Div(id='output-data-upload', style={'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '45px'}),
    ])
])


@callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')]
)


def update_output(contents):

    if contents is not None:
        content_type, content_string = contents.split(',')
        
        decoded = base64.b64decode(content_string)

        try:
            df_test = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            #print(df_test.head())
            loaded_model = pickle.load(open('best_model.pkl', 'rb'))
            pred = loaded_model.predict(df_test)
            #pred = pd.DataFrame(pred)
            df_label['label'] = " "
            for index, row in df_label.iterrows():
                number = row['Number']
                string = row['String']
                df_label.loc[df_label['Number'] == number, 'label'] = string

            df_assigned = pd.DataFrame({'Number': pred})
            df_assigned = pd.merge(df_assigned, df_label, on='Number', how='left')
            # Print the result
            result = df_assigned.drop(columns=['Number', 'String'])
            #result = LabelEncoder().inverse_transform(result)
            merged_df = pd.concat([df_test, result], axis=1)
            csv_string = merged_df.to_csv(index=False)
            csv_string = "data:text/csv;charset=utf-8," + quote(csv_string, safe='')

            return html.Div([
                html.A(
                    dbc.Button('Download Predictions', id="download-button", outline=True, color="danger"),
                    href=csv_string,
                    download="merged_data.csv"
                )
            ])

        except KeyError as e:
            error_message = f"KeyError: '{e.args[0]}' column not found in the uploaded file."
            return html.Div([
                html.P(error_message, style={'color': 'red'})
            ])
    return None