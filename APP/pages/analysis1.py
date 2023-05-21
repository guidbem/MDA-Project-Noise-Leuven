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
daily_data['month'] = daily_data['datetime'].dt.month

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
daily_data['month'] = daily_data['month'].map(month_mapping)

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
        html.H2("Highest lcpeak: "),
        html.P(id='text-output'),
        ], style={"position": "absolute", "zIndex": "1", "width": "2000px", "margin-left":"500px","margin-top":"80px"}
    ),
    html.Div(
    children=[
        html.H2("Noisest day: (average laeq)"),
        html.P(id='text-output-avg'),
        ], style={"position": "absolute", "zIndex": "1", "width": "2000px", "margin-left":"900px","margin-top":"80px"}
    ),
    html.Div(className="graph", style={"background-color": "#F5F5F5"}, children=[
        html.Div(style={"marginBottom": "10px", "display": "flex"}, children=[
            dbc.Button("Yearly Data", id="yearly-button", n_clicks=0, style={"margin-left": "1350px","margin-top": "0px","zIndex": "2"}, outline=False, color="danger", className="me-1"),
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
                "height": "1400px",
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
    dcc.Dropdown(
        id='month-dropdown2',
        options=dropdown_options,
        placeholder="Select a Month",
        style={"position": "absolute", "zIndex": "1", "width": "200px","margin-top":"30px"},
    ),
    html.Div([
        html.Div([
            dcc.Graph(id='heatmap-graph')
        ], style={'width': '500px', 'display': 'inline-block',"margin-left": "400px","margin-top": "50px"}),
        html.Div([
            dcc.Graph(id='donut-chart')
        ], style={'width': '400px', 'display': 'inline-block',"margin-left": "120px","margin-bottom": "50px"})
    ])
])

@callback(
    Output('text-output', 'children'),
    Output('text-output-avg', 'children'),
    Output('line-graph', 'figure'),
    Output('donut-chart', 'figure'),
    Output('heatmap-graph', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('month-dropdown2', 'value'),
     Input('yearly-button', 'n_clicks')]
)
def update_text(month1,month2, yearly_clicks):

    month=None
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "month-dropdown":
        month=month1

    if button_id == "month-dropdown2":
        month=month2

    if button_id == "month-dropdown" or button_id == "month-dropdown2":
        title_plot=f"Leuven Noise - {month} Data"
        filtered_df = hourly_data[hourly_data['month'] == month]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['laeq'], mode='lines', name='laeq',line=dict(color='navy')))
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['lceq'], mode='lines', name='lceq',line=dict(color='red')))
        
        filtered_df_donut = df_donut[df_donut['month'] == month]
        event_frequency = filtered_df_donut['noise_event_laeq_primary_detected_class'].value_counts()
        fig2 = go.Figure(data=go.Pie(
            labels=event_frequency.index,
            values=event_frequency.values,
            hole=0.4
        ))

        heatmap_data = filtered_df.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')
        fig3 = go.Figure(data=go.Heatmap(
            z=heatmap_data.values[::-1],
            x=heatmap_data.columns,
            y=heatmap_data.index[::-1],
            colorscale='Viridis'
        ))

        
        if month is None:
            formatted_date="",
            formatted_date_avg=""

        else:
            filtered_df = hourly_data[hourly_data['month'] == month]
            hour_with_highest_lcpeak = filtered_df.loc[filtered_df['lcpeak'].idxmax(), 'datetime']
            day_name = hour_with_highest_lcpeak.day
            weekday_name = hour_with_highest_lcpeak.strftime("%A")
            hour_name = hour_with_highest_lcpeak.strftime("%H:%M")
            max_value = filtered_df.lcpeak.max()
            formatted_date = f"{day_name} {weekday_name} at {hour_name} ({max_value}dB)"
            filtered_df = daily_data[daily_data['month'] == month]
            day_with_highest_laeq = filtered_df.loc[filtered_df['laeq'].idxmax(), 'datetime']
            day_name = day_with_highest_laeq.day
            weekday_name = day_with_highest_laeq.strftime("%A")
            max_value = round(filtered_df.laeq.max(),2)
            formatted_date_avg = f"{day_name} {weekday_name} ({max_value}dB)"

    else:
        # Yearly Data
        title_plot="Leuven Noise - Yearly Data"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_data['datetime'], y=daily_data['laeq'], mode='lines', name='laeq',line=dict(color='navy')))
        fig.add_trace(go.Scatter(x=daily_data['datetime'], y=daily_data['lceq'], mode='lines', name='lceq',line=dict(color='red')))
        
        event_frequency = df_donut['noise_event_laeq_primary_detected_class'].value_counts()
        fig2 = go.Figure(data=go.Pie(
            labels=event_frequency.index,
            values=event_frequency.values,
            hole=0.4
        ))

        heatmap_data = hourly_data.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')
        fig3 = go.Figure(data=go.Heatmap(
            z=heatmap_data.values[::-1],
            x=heatmap_data.columns,
            y=heatmap_data.index[::-1],
            colorscale='Viridis'
        ))

        day_with_highest_lcpeak = daily_data.loc[daily_data['lcpeak'].idxmax(), 'datetime']
        # Extract day name and weekday name
        day_name = day_with_highest_lcpeak.strftime("%B %d")
        weekday_name = day_with_highest_lcpeak.strftime("%A")
        max_value = daily_data.lcpeak.max()
        formatted_date = f"{day_name} {weekday_name} ({max_value}dB)"
        day_with_highest_laeq = daily_data.loc[daily_data['laeq'].idxmax(), 'datetime']
        day_name = day_with_highest_laeq.strftime("%B %d")
        weekday_name = day_with_highest_laeq.strftime("%A")
        max_value = round(daily_data.laeq.max(),2)
        formatted_date_avg = f"{day_name} {weekday_name} ({max_value}dB)"


    fig.update_layout(
        title={
            "text": f"<b>{title_plot}</b>",
        },
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        width=1100,
        height=480
    )

    fig2.update_layout(
        title='Event Frequency',
        height=400,
        width=500
    )

    fig3.update_layout(
        xaxis_title='Day of the Week',
        yaxis_title='Time',
        title='Hourly Heatmap',
        height=600,
        width=600
    )

    return formatted_date, formatted_date_avg,fig,fig2,fig3