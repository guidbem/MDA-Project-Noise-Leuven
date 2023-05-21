from dateutil import parser
import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/analysis-1')


df = pd.read_parquet("mergedfile.parquet")
df['datetime'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour']+":"+df["min"]+":00")
df.set_index('datetime', inplace=True)

# Resample the data to hourly frequency
hourly_data = df.resample('H').agg({'laeq': 'mean', 'lceq': 'mean', 'lamax': 'max', 'lcpeak': 'max'})
# Reset the index to make the datetime column a regular column again
hourly_data.reset_index(inplace=True)
hourly_data['month'] = hourly_data['datetime'].dt.month
hourly_data['time'] = hourly_data['datetime'].dt.time
hourly_data['day_of_week'] = hourly_data['datetime'].dt.weekday
hourly_data.dropna()
# Resample the data to daily frequency
daily_data = df.resample('D').agg({'laeq': 'mean', 'lceq': 'mean', 'lamax': 'max', 'lcpeak': 'max'})
# Reset the index to make the datetime column a regular column again
daily_data.reset_index(inplace=True)

# Default month
month="January"

# Create a dictionary mapping numerical values to month names
day_mapping = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

# Use the map function to replace numerical values with month names
hourly_data['day_of_week'] = hourly_data['day_of_week'].map(day_mapping)
hourly_data['day_of_week'] = pd.Categorical(hourly_data['day_of_week'], 
                                       categories=['Sunday', 'Monday', 'Tuesday', 
                                                   'Wednesday', 'Thursday', 'Friday', 'Saturday'], 
                                       ordered=True)

# Create a dictionary mapping numerical values to month names
month_mapping = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

# Use the map function to replace numerical values with month names
hourly_data['month'] = hourly_data['month'].map(month_mapping)

df_donut = pd.read_csv("doughnut_data.csv")
# Drop rows with values 'Not Available' and 'Unsupported' in the noise event type column
df_donut = df_donut[~df_donut['noise_event_laeq_primary_detected_class'].isin(['Not Available', 'Unsupported'])]


# Create the dropdown menu options
dropdown_options = [{'label': month, 'value': month} for month in ['January', "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", 'December']]


# Define the styles for the dropdown menu
dropdown_style = {
    'width': '50px',
    'height': '30px',
    'padding': '5px',
    'border-radius': '5px',
    'border': '1px solid #ccc',
    'font-size': '14px',
    'color': '#333',
    'background-color': '#fff',
    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
    'transform': 'scale(0.8)',
    'transform-origin': 'top left'
}


# Define the styles for the dropdown menu options
option_style = {
    'padding': '8px',
    'font-size': '12px'
}

# Define the layout

layout = html.Div([

    dcc.Dropdown(
        id='month-dropdown',
        options=dropdown_options,
        placeholder="Select a Month",
        style={"position": "absolute", "zIndex": "1", "width": "200px"},
    ),
    html.Div(
    children=[
        html.H2("Highest lcpeak:"),
        html.P(id='text-output'),
        ], style={"position": "absolute", "zIndex": "1", "width": "2000px", "margin-left":"400px","margin-top":"80px"}
    ),
    html.Div(className="graph", style={"background-color": "#F5F5F5"}, children=[
        html.Div(style={"marginBottom": "10px", "display": "flex", "justify-content": "flex-end"}, children=[
            dbc.Button("Yearly Data", id="yearly-button", n_clicks=0, style={"margin-right": "50px","margin-top": "0px","zIndex": "2"}, outline=False, color="danger", className="me-1"),
            dbc.Button("Monthly Data", id="monthly-button", n_clicks=0, style={"margin-right": "25px","margin-top": "0px","zIndex": "0"},outline=False, color="danger", className="me-1"),
        ]),
        dcc.Graph(id="line-graph", style={"margin-left": "400px","margin-top": "180px"}),
        html.Div(
            style={
                "position": "absolute",
                "left": "0",
                "top": "68px",
                "width": "100%",
                "height": "2px",
                "backgroundColor": "lightgray",
                "zIndex": "0"
            }
        ),
        html.Div(
            style={
                "position": "absolute",
                "left": "330px",
                "top": "68px",
                "width": "1px",
                "height": "700px",
                "backgroundColor": "lightgray",
                "zIndex": "0"
            }
        ),
        html.Div(
            style={
                "position": "absolute",
                "left": "0",
                "top": "766px",
                "width": "100%",
                "height": "2px",
                "backgroundColor": "lightgray",
                "zIndex": "0"
            }
        ),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='heatmap-graph')
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='donut-chart')
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
])


@callback(
    Output('heatmap-graph', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('yearly-button', 'n_clicks'),
     Input('monthly-button', 'n_clicks')]
)
def update_heatmap(month, yearly_clicks, monthly_clicks):    
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    filtered_df = hourly_data[hourly_data['month'] == month]
    heatmap_data = filtered_df.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')
    
    if button_id == "monthly-button":
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values[::-1],
            x=heatmap_data.columns,
            y=heatmap_data.index[::-1],
            colorscale='Viridis'
        ))

    elif button_id == "month-dropdown":
        filtered_df = hourly_data[hourly_data['month'] == month]
        heatmap_data = filtered_df.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values[::-1],
            x=heatmap_data.columns,
            y=heatmap_data.index[::-1],
            colorscale='Viridis'
        ))
    
    else:
        heatmap_data = hourly_data.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values[::-1],
            x=heatmap_data.columns,
            y=heatmap_data.index[::-1],
            colorscale='Viridis'
        ))

    fig.update_layout(
        xaxis_title='Day of the Week',
        yaxis_title='Time',
        title='Hourly Heatmap',
        height=600,
        width=600
    )
    return fig

@callback(
    dash.dependencies.Output('donut-chart', 'figure'),
    [dash.dependencies.Input('month-dropdown', 'value'),
     Input('yearly-button', 'n_clicks'),
     Input('monthly-button', 'n_clicks')]
)
def update_donut(month, yearly_clicks, monthly_clicks):
        
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    filtered_df_donut = df_donut[df_donut['month'] == month]
    event_frequency = filtered_df_donut['noise_event_laeq_primary_detected_class'].value_counts()
    if button_id == "monthly-button":
        fig = go.Figure(data=go.Pie(
            labels=event_frequency.index,
            values=event_frequency.values,
            hole=0.4
        ))
    elif button_id == "month-dropdown":
        filtered_df_donut = df_donut[df_donut['month'] == month]
        event_frequency = filtered_df_donut['noise_event_laeq_primary_detected_class'].value_counts()
        fig = go.Figure(data=go.Pie(
            labels=event_frequency.index,
            values=event_frequency.values,
            hole=0.4
        ))
    else:
        event_frequency = df_donut['noise_event_laeq_primary_detected_class'].value_counts()
        fig = go.Figure(data=go.Pie(
            labels=event_frequency.index,
            values=event_frequency.values,
            hole=0.4
        ))

    fig.update_layout(
        title='Event Frequency',
        height=400,
        width=500
    )
    return fig


@callback(
    Output('line-graph', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('yearly-button', 'n_clicks'),
     Input('monthly-button', 'n_clicks')]
)
def update_line(month, yearly_clicks, monthly_clicks):

    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    filtered_df = hourly_data[hourly_data['month'] == month]
    if button_id == "monthly-button":
        title_plot=f"Leuven Noise - {month} Data"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['laeq'], mode='lines', name='laeq',line=dict(color='navy')))
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['lceq'], mode='lines', name='lceq',line=dict(color='red')))

    elif button_id == "month-dropdown":
        title_plot=f"Leuven Noise - {month} Data"
        filtered_df = hourly_data[hourly_data['month'] == month]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['laeq'], mode='lines', name='laeq',line=dict(color='navy')))
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['lceq'], mode='lines', name='lceq',line=dict(color='red')))

    else:
        # Yearly Data
        title_plot="Leuven Noise - Yearly Data"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_data['datetime'], y=daily_data['laeq'], mode='lines', name='laeq',line=dict(color='navy')))
        fig.add_trace(go.Scatter(x=daily_data['datetime'], y=daily_data['lceq'], mode='lines', name='lceq',line=dict(color='red')))


    fig.update_layout(
        title={
            "text": f"<b>{title_plot}</b>",
        },
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        width=1100,
        height=480
    )
    return fig

@callback(
    Output('text-output', 'children'),
    [Input('month-dropdown', 'value'),
     Input('yearly-button', 'n_clicks'),
     Input('monthly-button', 'n_clicks')]
)
def update_text(month, yearly_clicks, monthly_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    filtered_df = hourly_data[hourly_data['month'] == month]

    if button_id == "monthly-button":
        if month is None:
            formatted_date=""

        else:
            hour_with_highest_lcpeak = filtered_df.loc[filtered_df['lcpeak'].idxmax(), 'datetime']
            day_name = hour_with_highest_lcpeak.day
            weekday_name = hour_with_highest_lcpeak.strftime("%A")
            hour_name = hour_with_highest_lcpeak.strftime("%H:%M")
            formatted_date = f"{day_name} {weekday_name} at {hour_name}"

    elif button_id == "month-dropdown":
        filtered_df = hourly_data[hourly_data['month'] == month]
        hour_with_highest_lcpeak = filtered_df.loc[filtered_df['lcpeak'].idxmax(), 'datetime']
        day_name = hour_with_highest_lcpeak.day
        weekday_name = hour_with_highest_lcpeak.strftime("%A")
        hour_name = hour_with_highest_lcpeak.strftime("%H:%M")
        formatted_date = f"{day_name} {weekday_name} at {hour_name}"

    else:
        day_with_highest_lcpeak = daily_data.loc[daily_data['lcpeak'].idxmax(), 'datetime']
        # Extract day name and weekday name
        day_name = day_with_highest_lcpeak.strftime("%B %d")
        weekday_name = day_with_highest_lcpeak.strftime("%A")
        formatted_date = f"{day_name} {weekday_name}"

    return formatted_date