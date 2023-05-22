from dateutil import parser
import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

# Register the page for analysis 1
dash.register_page(__name__, path='/analysis-1')

# Load the data and convert date, hour, and minute columns to datetime
df = pd.read_parquet("mergedfile.parquet")
df['datetime'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour']+":"+df["min"]+":00")
df.set_index('datetime', inplace=True)

# Resample the data to hourly frequency and calculate the mean and max values
hourly_data = df.resample('H').agg({'laeq': 'mean', 'lceq': 'mean', 'lamax': 'max', 'lcpeak': 'max'})

# Reset the index to make the datetime column a regular column again
hourly_data.reset_index(inplace=True)
hourly_data['month'] = hourly_data['datetime'].dt.month
hourly_data['time'] = hourly_data['datetime'].dt.time
hourly_data['day_of_week'] = hourly_data['datetime'].dt.weekday
hourly_data.dropna()

# Resample the data to daily frequency and calculate the mean and max values
daily_data = df.resample('D').agg({'laeq': 'mean', 'lceq': 'mean', 'lamax': 'max', 'lcpeak': 'max'})

# Reset the index to make the datetime column a regular column again
daily_data.reset_index(inplace=True)
daily_data['month'] = daily_data['datetime'].dt.month

# Create a dictionary mapping numerical values to month names
day_mapping = {
    0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
    4: "Friday", 5: "Saturday", 6: "Sunday",}

# Use the map function to replace numerical values with month names
hourly_data['day_of_week'] = hourly_data['day_of_week'].map(day_mapping)
hourly_data['day_of_week'] = pd.Categorical(hourly_data['day_of_week'], 
                                            categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 
                                            ordered=True)

# Create a dictionary mapping numerical values to month names
month_mapping = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

# Use the map function to replace numerical values with month names
hourly_data['month'] = hourly_data['month'].map(month_mapping)
daily_data['month'] = daily_data['month'].map(month_mapping)

# Load the data for the donut chart from a CSV file
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

# The styles of the boxes
box_style_lcpeak = {
    'height':'100px',
    'width':'300px',
    'background-color': 'lightblue',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '100px',
    'left': '350px'
}

box_style_avg_laeq = {
    'height':'100px',
    'width':'300px',
    'background-color': 'lightgreen',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '100px',
    'right': '350px'
}

# Define the layout
layout = html.Div([
    # First dropdown menu for selecting a month
    dcc.Dropdown(
        id='month-dropdown',
        options=dropdown_options,
        placeholder="Select a Month",
        style={"position": "absolute", "zIndex": "1", "width": "200px"},
    ),

    # Interactive Text for displaying the highest lcpeak
    html.Div(
    children=[
        html.H2("Highest lcpeak: "),
        html.P(id='text-output'),
        ], style= box_style_lcpeak
    ),

    # Interactive Text for displaying the noisiest day
    html.Div(
    children=[
        html.H2("Noisest day:"),
        html.P(id='text-output-avg'),
        ], style= box_style_avg_laeq
    ),

    # Line plot graph
    html.Div(className="graph", style={"background-color": "#F5F5F5"}, children=[
        html.Div(style={"marginBottom": "10px", "display": "flex"}, children=[
            dbc.Button("Yearly Data", id="yearly-button", n_clicks=0, style={"margin-left": "1350px","margin-top": "0px","zIndex": "2"}, outline=False, color="danger", className="me-1"),
        ]), 
        dcc.Graph(id="line-graph", style={"margin-left": "400px","margin-top": "180px"}),

        # Horizontal line
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

        # Vertical Line 
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

        # Horizontal line
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

    # Second dropdown menu for selecting a month
    dcc.Dropdown(
        id='month-dropdown2',
        options=dropdown_options,
        placeholder="Select a Month",
        style={"position": "absolute", "zIndex": "1", "width": "200px","margin-top":"30px"},
    ),

    html.Div([ 
        # Heatmap graph
        html.Div([
            dcc.Graph(id='heatmap-graph')
        ], style={'width': '500px', 'display': 'inline-block',"margin-left": "400px","margin-top": "50px"}),

        # Donut chart graph
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

    # Initialise the month variable
    month=None

    # Save the id of the pressed button
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Check which dropdown was triggered
    if button_id == "month-dropdown":
        month=month1

    if button_id == "month-dropdown2":
        month=month2

    # Update the text, line graph, donut chart, and heatmap based on the selected month
    if button_id == "month-dropdown" or button_id == "month-dropdown2":
        title_plot=f"Leuven Noise - {month} Data"

        # Filter the data based on the selected month
        filtered_df = hourly_data[hourly_data['month'] == month]
        
        # Create the line graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['laeq'], mode='lines', name='laeq',line=dict(color='navy')))
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['lceq'], mode='lines', name='lceq',line=dict(color='red')))
        
        # Create the donut chart
        filtered_df_donut = df_donut[df_donut['month'] == month]
        event_frequency = filtered_df_donut['noise_event_laeq_primary_detected_class'].value_counts()
        donut_fig = go.Figure(data=go.Pie(
            labels=event_frequency.index,
            values=event_frequency.values,
            hole=0.4
        ))

        # Create the heatmap
        heatmap_data = filtered_df.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values[::-1],
            x=heatmap_data.columns,
            y=heatmap_data.index[::-1],
            colorscale='Viridis'
        ))


        # Initialize variables to keep the formatted date and average empty if no month is selected
        if month is None:
            formatted_date="",
            formatted_date_avg=""

        # Calculate and format the highest lcpeak and noisiest day values for the text
        else:

            # Find the hour with the highest lcpeak and extract relevant information
            hour_with_highest_lcpeak = filtered_df.loc[filtered_df['lcpeak'].idxmax(), 'datetime']
            day_name = hour_with_highest_lcpeak.day
            weekday_name = hour_with_highest_lcpeak.strftime("%A")
            hour_name = hour_with_highest_lcpeak.strftime("%H:%M")
            max_value = filtered_df.lcpeak.max()
            formatted_date = f"{day_name} {weekday_name} at {hour_name} ({max_value}dB)"

            # Filter the daily data based on the selected month to find the day with the highest laeq and extract relevant information
            filtered_df = daily_data[daily_data['month'] == month]
            day_with_highest_laeq = filtered_df.loc[filtered_df['laeq'].idxmax(), 'datetime']
            day_name = day_with_highest_laeq.day
            weekday_name = day_with_highest_laeq.strftime("%A")
            max_value = round(filtered_df.laeq.max(),2)
            formatted_date_avg = f"{day_name} {weekday_name} ({max_value}dB)"

    else:
        # Yearly Data
        title_plot="Leuven Noise - Yearly Data"

        # Create the line graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_data['datetime'], y=daily_data['laeq'], mode='lines', name='laeq',line=dict(color='navy')))
        fig.add_trace(go.Scatter(x=daily_data['datetime'], y=daily_data['lceq'], mode='lines', name='lceq',line=dict(color='red')))
        
        # Create the donut chart after calculating the event frequency
        event_frequency = df_donut['noise_event_laeq_primary_detected_class'].value_counts()
        donut_fig = go.Figure(data=go.Pie(
            labels=event_frequency.index,
            values=event_frequency.values,
            hole=0.4
        ))

        # Create the heatmap using all year data
        heatmap_data = hourly_data.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values[::-1],
            x=heatmap_data.columns,
            y=heatmap_data.index[::-1],
            colorscale='Viridis'
        ))

        # Find the day with the highest lcpeak and extract relevant information
        day_with_highest_lcpeak = daily_data.loc[daily_data['lcpeak'].idxmax(), 'datetime']
        day_name = day_with_highest_lcpeak.strftime("%B %d")
        weekday_name = day_with_highest_lcpeak.strftime("%A")
        max_value = daily_data.lcpeak.max()
        formatted_date = f"{day_name} {weekday_name} ({max_value}dB)"

        # Find the day with the highest laeq and extract relevant information
        day_with_highest_laeq = daily_data.loc[daily_data['laeq'].idxmax(), 'datetime']
        day_name = day_with_highest_laeq.strftime("%B %d")
        weekday_name = day_with_highest_laeq.strftime("%A")
        max_value = round(daily_data.laeq.max(),2)
        formatted_date_avg = f"{day_name} {weekday_name} ({max_value}dB)"

    # Update layout for the line graph
    fig.update_layout(
        title={
            "text": f"<b>{title_plot}</b>",
        },
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        width=1100,
        height=480
    )

    # Update layout for the donut chart
    donut_fig.update_layout(
        title='Event Frequency',
        height=400,
        width=500
    )

    # Update layout for the heatmap 
    heatmap_fig.update_layout(
        xaxis_title='Day of the Week',
        yaxis_title='Time',
        title='Hourly Heatmap',
        height=600,
        width=600
    )

    # Return the formatted date, formatted average date, line graph, donut chart, and heatmap graph
    return formatted_date, formatted_date_avg, fig, donut_fig, heatmap_fig