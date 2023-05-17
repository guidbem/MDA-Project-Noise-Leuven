import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc, callback, Input, Output


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

# Define the layout of the app
layout = html.Div([
    dcc.Dropdown(
        id='month-dropdown',
        options=dropdown_options,
        placeholder="Select a Month"       
    ),
    dcc.Graph(id='heatmap-graph'),
    dcc.Graph(id='donut-chart')
])


@callback(
    dash.dependencies.Output('heatmap-graph', 'figure'),
    [dash.dependencies.Input('month-dropdown', 'value')]
)
def update_heatmap(month):
    filtered_df = hourly_data[hourly_data['month'] == month]
    heatmap_data = filtered_df.pivot_table(index='time', columns='day_of_week', values='laeq', aggfunc='mean')

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
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
    [dash.dependencies.Input('month-dropdown', 'value')]
)
def update_donut(month):
    filtered_df_donut = df_donut[df_donut['month'] == month]
    event_frequency = filtered_df_donut['noise_event_laeq_primary_detected_class'].value_counts()

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