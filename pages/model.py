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

dash.register_page(__name__, path='/model')

# Classification table
classification_report_data = {
    'Class': ['Human voice - Shouting', 'Human voice - Singing', 'Other', 'Transport road - Passenger car', 'Transport road - Siren', ' ', 'accuracy', 'macro avg', 'weighted avg'],
    'Precision': [0.41, 0.12, 0.51, 0.88, 0.33, ' ', '-', 0.45, 0.72],
    'Recall': [0.68, 0.62, 0.37, 0.77, 0.77, ' ', '-', 0.64, 0.65],
    'F1-Score': [0.51, 0.20, 0.43, 0.82, 0.47, ' ', 0.65, 0.49, 0.67],
    'Support': [1671, 352, 6224, 14301, 622, ' ', 23170, 23170, 23170]
}
classification_report_df = pd.DataFrame(classification_report_data)

feat_imp = '/assets/feature_importance.png'
conf_mat = '/assets/confusion_matrix.png'
roc = '/assets/ROC_curves.png'
balanced_accuracy = 64.3

# Mapping of class numbers to their corresponding labels
label = {
    'Number': [0, 1, 2, 3, 4],
    'String': ['Human voice - Shouting', 'Human voice - Singing', 'Other', 'Transport road - Passenger car', 'Transport road - Siren']
}
df_label = pd.DataFrame(label)


# Define the layout
layout = html.Div([
    html.P(['This page sumarizes the results obtained for the LightGBM model, which was the model that gave the best results with a balanced accuracy of 64.30%.'],
           style={'margin-left':'20px', 'margin-top':'10px'}),

    html.Ul([
        html.Li("The Classification Report Table provides an overview of the model's performance across the various classes."),
        html.Li("The Feature Importance allows to identify the features that have the most significant impact on the model's predictions."),
        html.Li("The Confusion Matrix offers a visual representation of predicted labels compared to the actual labels."),
        html.Li("The ROC Curves, using the One-vs-Rest approach, illustrates how well the model can differentiate between different classes,."),
            ],style={'margin-left':'20px'}),

    html.P(['The Predictions section allows users to upload a CSV file containing data for which labels need to be predicted. It employs a pre-trained model (the model mentioned previously) to generate predictions for the uploaded data. The predicted labels are then merged with the original data and made available for download as a CSV file. Additionally, the label counts table provides a summary of the frequency of each predicted label.'],
           style={'margin-left':'20px', 'margin-bottom':'20px'}),

    dbc.Row([
        dbc.Col([
            html.H3('Classification Report', style={'margin-left':'50px', 'margin-top':'10px'}),

            # Create a table to display the classification report
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

            # Create a card to display the Balanced Accuracy
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Balanced accuracy", className="card-title"),
                        html.H3(f"{balanced_accuracy:.2f} %", className="card-text"),
                    ])
                ], className="mb-4", style={'backgroundColor':'rgba(255, 0, 0, 0.4)', "margin": "auto", "maxWidth": "fit-content", "padding": "10px"})
            ]),
        ], width=6), 

        # Confusion Matrix image
        dbc.Col([
            html.H3('Feature Importance', style={'margin-left':'120px', 'margin-top':'10px'}),
            html.Img(src=feat_imp, style={'width': '430px', 'margin-left':'120px', 'border': '1px solid black', 'margin-top':'10px'})
        ], width=6)
    ], style={'background-color': '#F5F5F5'}),

  dbc.Row([
    # Confusion Matrix
    dbc.Col([
        html.H3('Confusion Matrix', style={'margin-left': '150px', 'margin-top': '50px'}),
        html.Img(src=conf_mat, style={'width': '490px', 'margin-left': '150px', 'border': '1px solid black', 'margin-top': '10px'})
    ], width=6),

    # ROC curves
    dbc.Col([
        html.H3('ROC curves', style={'margin-left': '120px', 'margin-top': '50px'}),
        html.Img(src=roc, style={'width': '500px', 'margin-left': '120px', 'border': '1px solid black', 'margin-top': '10px','margin-bottom': '20px'})
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

            # Upload button
            dcc.Upload(
                id="upload-data",
                children=html.Div([
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
                    'margin-bottom': '20px',
                    'display': 'inline-block'
                },
                multiple=False
            ),
        ], style={'display': 'inline-block'}),
        html.Div(id='output-data-upload', style={'margin-left': '20px', 'margin-top': '10px'}),
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
            df_test = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Loading the saved model (LightGBM)
            loaded_model = pickle.load(open('data/best_model.pkl', 'rb'))

            # Predicting the labels
            pred = loaded_model.predict(df_test)

            # Iterate over df_label DataFrame to assign labels based on 'Number' column
            df_label['label'] = " "
            for index, row in df_label.iterrows():
                number = row['Number']
                string = row['String']
                df_label.loc[df_label['Number'] == number, 'label'] = string

            df_assigned = pd.DataFrame({'Number': pred})

            # Merge predicted labels with original labels
            df_assigned = pd.merge(df_assigned, df_label, on='Number', how='left')

            # Drop unnecessary columns from the result
            result = df_assigned.drop(columns=['Number', 'String'])

            # Concatenate original data with result
            merged_df = pd.concat([df_test, result], axis=1)

            # Calculate label counts
            label_counts = result['label'].value_counts().reset_index()
            label_counts.columns = ['Label', 'Count']

            # Format CSV string for download
            csv_string = merged_df.to_csv(index=False)
            csv_string = "data:text/csv;charset=utf-8," + quote(csv_string, safe='')

            # Display a link to download the merged data as a CSV file
            return html.Div([
                html.A(
                    dbc.Button('Download Predictions', id="download-button", outline=True, color="danger", style={'margin-top': '-20px'}),
                    href=csv_string,
                    download="merged_data.csv",
                ),
                html.H4('Label Counts', style={'margin-top': '25px'}),
                dash_table.DataTable(
                    id='label-counts-table',
                    columns=[{"name": i, "id": i} for i in label_counts.columns],
                    data=label_counts.to_dict('records'),
                    style_table={'max-width': '300px',  # Set the maximum width of the table
                                 'margin-left': '0px',
                                 'margin-bottom': '30px',
                                 'font-size': '14px',
                                 'border-collapse': 'collapse',
                                 'border-spacing': '0',
                                 'text-align': 'center'},
                    style_header={
                        'background-color': 'rgba(0, 0, 0, 0.1)',
                        'font-weight': 'bold',
                    },
                    style_cell={
                        'background-color': 'rgba(255, 255, 255, 1)',
                    },
                )
            ])

        except KeyError as e:
            error_message = f"KeyError: '{e.args[0]}' column not found in the uploaded file."
            # Display an error message if the required column is not found in the uploaded file
            return html.Div([
                html.P(error_message, style={'color': 'red'})
            ])
    return None