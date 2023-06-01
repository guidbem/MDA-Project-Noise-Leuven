from dateutil import parser
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

# Register the page for analysis 1
dash.register_page(__name__, path='/analysis-1')

# Load the data and convert date, hour, and minute columns to datetime
df = pd.read_parquet("noise_minutes.parquet")
df = df.sort_values(by=["date","hour","min"])
df['datetime'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour'], unit="h")  +pd.to_timedelta(df["min"], unit="m")
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


# Load the data for the donut chart from a CSV file
df_events = pd.read_csv("doughnut_data.csv")

# Convert result_timestamp to datetime format
df_events['result_timestamp_datetime'] = pd.to_datetime(df_events['result_timestamp'], dayfirst=True)
# Extract month, hour, and date
df_events['month'] = df_events['result_timestamp_datetime'].dt.month.map(month_mapping)
df_events['hour'] = df_events['result_timestamp_datetime'].dt.hour
df_events['date'] = df_events['result_timestamp_datetime'].dt.date
# Convert result_timestamp_datetime to string format
df_events['result_timestamp_datetime'] = df_events['result_timestamp_datetime'].dt.strftime('%Y-%m-%d %H:00:00')

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
    'height':'120px',
    'width':'300px',
    'background-color': 'rgb(225,0,0,0.1)',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '140px',
    'left': '450px',
    'border': '2px solid red',
    "zIndex": "1",
}

box_style_avg_laeq = {
    'height':'125px',
    'width':'300px',
    'background-color': 'rgb(225,0,0,0.1)',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '140px',
    'right': '230px',
    'border': '2px solid red',
    "zIndex": "1",
}

box_style_content = {
    'height':'400px',
    'width':'300px',
    'background-color': 'rgb(225,0,0,0.1)',
    'padding': '10px',
    'border-radius': '5px',
    'margin-bottom': '10px',
    'position': 'absolute',
    'top': '950px',
    'left': '15px',
    'border': '2px solid red'

}

# Define the layout
layout = html.Div([
    html.H3('Visual Analysis', style={"position": "absolute","font-size": "34px",'margin-left':'670px', 'margin-top':'10px',"zIndex": "1","text-align": "center","color": "#dc3545","fontWeight": "bold",}),
    # First dropdown menu for selecting a month
    dcc.Dropdown(
        id='month-dropdown',
        options=dropdown_options,
        placeholder="Select a Month",
        style={"position": "absolute", "zIndex": "1", "width": "200px","margin-top":"20px","margin-right":"10px"},
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
        html.H2("Noisiest day:"),
        html.P(id='text-output-avg'),
        ], style= box_style_avg_laeq
    ),
    # Interactive Text for every month content
    html.Div(
    children=[
        html.H2("Some information"),
        html.P(id='text-output-content'),
        ], style= box_style_content
    ),

    # Line plot graph
    html.Div(className="graph", style={"background-color": "#F5F5F5"}, children=[
        html.Div(style={"marginBottom": "10px", "display": "flex"}, children=[
            dbc.Button("Yearly Data", id="yearly-button", n_clicks=0, style={"margin-left": "1350px","margin-top": "20px","zIndex": "2"}, outline=False, color="danger", className="me-1"),
        ]), 
        dcc.Graph(id="line-graph", style={"margin-left": "400px","margin-top": "120px"}),
    ]),
        
    # Lightgrey lines
    html.Div(children=[
        # Horizontal line
        html.Div( style={"position": "absolute", "left": "0", "top": "68px", "width": "100%", "height": "2px", "backgroundColor": "lightgray", "zIndex": "0"}),

        # Vertical Line 
        html.Div(style={"position": "absolute", "left": "330px", "top": "68px", "width": "1px", "height": "1400px", "backgroundColor": "lightgray", "zIndex": "0"}),

        # Horizontal line
        html.Div(style={"position": "absolute","left": "0","top": "826px","width": "100%","height": "2px","backgroundColor": "lightgray","zIndex": "0"}),
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
    Output('text-output-content', 'children'),
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
        filtered_event_df = df_events[df_events['month'] == month]

        # Calculate the number of events per hour
        df_event_counts = filtered_event_df.groupby(['result_timestamp_datetime', 'hour']).size().reset_index(name='event_count')

        # Create the line graph
        fig = go.Figure()

        
        fig.add_trace(go.Scatter(x=filtered_df['datetime'], y=filtered_df['laeq'], mode='lines', name='laeq',line=dict(color='#457b9d')))
        fig.add_trace(go.Scatter(x=[filtered_df.loc[filtered_df['laeq'].idxmax(), 'datetime']], y=[filtered_df.laeq.max()], mode='markers', name='Noisiest hour', marker=dict(color='#8B1A1A', size=10)))
        fig.add_trace(go.Scatter(x=[filtered_df.loc[filtered_df['laeq'].idxmin(), 'datetime']], y=[filtered_df.laeq.min()], mode='markers', name='Quietest hour', marker=dict(color='#FF7D40', size=10)))
        fig.add_trace(go.Bar(x=df_event_counts['result_timestamp_datetime'], y=(df_event_counts['event_count'])/6, name='Number of events', base=20, marker=dict(color='green'),text=df_event_counts['event_count']))

        # Filter the rows for Mondays
        filtered_df = filtered_df.copy()
        filtered_df.loc[:, 'weekday'] = filtered_df['datetime'].dt.weekday
        filtered_df.loc[:, 'hour'] = filtered_df['datetime'].dt.hour
        mondays_filtered_df = filtered_df[(filtered_df['weekday'] == 0) & (filtered_df['hour'] == 0)]  # 0 corresponds to Monday

        # Add vertical lines at the start of each for Monday
        for _, row in mondays_filtered_df.iterrows():
            line_datetime = row['datetime']
            fig.add_shape(
            type="line",
            x0=line_datetime,
            y0=20,
            x1=line_datetime,
            y1=65,
            line=dict(color="#a8a8a8", width=1, dash="solid"),
        )
            
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

            # Find the hour with the highest lcpeak and extract information
            hour_with_highest_lcpeak = filtered_df.loc[filtered_df['lcpeak'].idxmax(), 'datetime']
            day_name = hour_with_highest_lcpeak.day
            weekday_name = hour_with_highest_lcpeak.strftime("%A")
            hour_name = hour_with_highest_lcpeak.strftime("%H:%M")
            max_value = filtered_df.lcpeak.max()
            formatted_date = f"{month} {day_name} {weekday_name}, at {hour_name} ({max_value}dB)"

            # Filter the daily data based on the selected month to find the day with the highest laeq and extract information
            filtered_df = daily_data[daily_data['month'] == month]
            day_with_highest_laeq = filtered_df.loc[filtered_df['laeq'].idxmax(), 'datetime']
            day_name = day_with_highest_laeq.day
            weekday_name = day_with_highest_laeq.strftime("%A")
            max_value = round(filtered_df.laeq.max(),2)
            formatted_date_avg = f"{month} {day_name}, {weekday_name} ({max_value}dB)"

    else:
        # Yearly Data
        title_plot="Leuven Noise - Yearly Data"

        # Create the line graph
        fig = go.Figure()

        df_event_counts = df_events.groupby('date').size().reset_index(name='event_count')
        
        fig.add_trace(go.Scatter(x=daily_data['datetime'],y=daily_data['laeq'],mode='lines',fill='toself',name='laeq',line=dict(color='#457b9d')))        
        fig.add_trace(go.Scatter(x=[daily_data.loc[daily_data['laeq'].idxmax(), 'datetime']], y=[daily_data.laeq.max()], mode='markers', name='Noisiest day', marker=dict(color='#8B1A1A', size=10)))
        fig.add_trace(go.Scatter(x=[daily_data.loc[daily_data['laeq'].idxmin(), 'datetime']], y=[daily_data.laeq.min()], mode='markers', name='Quietest day', marker=dict(color='#FF7D40', size=10)))
        fig.add_trace(go.Bar(x=df_event_counts['date'], y=(df_event_counts['event_count'])/100, name='Number of events', base=35, marker=dict(color='green'),text=df_event_counts['event_count']))

        # Get the last day of each month for the x-axis
        monthly_first_days = daily_data.groupby(pd.Grouper(key='datetime', freq='MS')).first().reset_index()

        # Add vertical lines at the end of each month
        for _, row in monthly_first_days.iterrows():
            line_datetime = row['datetime']
            fig.add_shape(
            type="line",
            x0=line_datetime,
            y0=35,
            x1=line_datetime,
            y1=57,
            line=dict(color="#a8a8a8", width=1, dash="solid"),
        )
        
        # Update layout for the line graph
        fig.update_layout(
            title={
                "text": f"<b>{title_plot}</b>",
            },
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            width=1100,
            height=580,
            xaxis=dict(
            title="Month",
            tickmode='array',
            tickvals=monthly_first_days['datetime'].dt.to_pydatetime(),
            ticktext=monthly_first_days['datetime'].dt.strftime('%b %Y'),
            tickangle=45
            ),
        )

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

        # Extract the maximum value from the heatmap
        
        max_heatmap_value = np.nanmax(heatmap_data.values)

     # Content update for every month
        
    if month == "January":
        formatted_content = "In January, the nights are generally very quiet throughout the month. The noisiest time was Thursdays around 13h00. Also, it is noticed that during Fridays, the noise continues more till midnight, unlike the other days of the week. The weekends are generally the most quiet time of the month, with only little noise occuring in the evening."
    elif month == "February":
        formatted_content = "In February, the nights are generally quiet throughout the month. The noisiest time of the month was Fridays in the entire month around 08h00. Also, it is noticed that during Thursdays and Fridays the noise tends to continue until midnight, before becoming very silent in the night. The weekends were comparatively more quiet than the other week-days, although some noise were recorded during the evenings of both Saturdays and Sundays."
    elif month == "March":
        formatted_content = " In March, there were some high levels of noise that was recorded throughout the day. The early Mondays and late night Sundays were the most quiet time during the day. The noisiest time was Monday mornings around 08h00. The nights are not as quiet as January and February. Late night noise were recorded during Wednesdays, Thursdays and Fridays. The weekends are comparatively more silent than the other days of the week during this month."
    elif month == "April":
        formatted_content = "In April, like March some high levels of noise were recorded throughout the entire day. The early Mondays and late night Sundays were the most quiet time during the day. The noisiest time of the month was early morning Tuesdays around 08h00. Noise continued late Thursday nights till early Friday mornings. The weekends are comparatively very quiet than the other days of the week during this month."
    elif month == "May":
        formatted_content = "In May, most nights were quiet with some exception. During, late night Wednesdays and early morning Thursdays, some high-levels of noise were recorded. The noisiest time was Tuesdays around 10h00. The weekends were comparatively less noisy than other days of the week, although some noise were recorded during the Saturdays."
    elif month == "June":
        formatted_content = "In June, the nights are generally very quiet. The noisiest time of month was Tuesdays around 10h00. It is noticed that during Thursdays, Fridays and Saturdays the noise continues till midnight unlike other days of the week. During the Sundays, the some noise was recorded in the Sunday evenings."
    elif month == "July":
        formatted_content = "In July, the nights are generally very silent. The noisiest time of the month was Thursdays around 12h00. It is noticed that during late Friday nights and early Saturday mornings there is a continuation of noise throughout the night."
    elif month == "August":
        formatted_content = "In August, like July, the nights are very silent with some exceptions. Some high levels of noise were recorded during the late Friday evenings and early Saturday mornings. The noisiest time of the month was during the Fridays around 11h00. During Saturday evenings some higher form of noise were recorded during the day."
    elif month == "September":
        formatted_content = "In September, the nights are very quiet throughout the entire month. The noisiest time of the month was Wednesdays around 08h00. It can be observed that during Thursdays and Fridays some form of noise continues till the midnight, unlike other days of week. The weekends are generally very quiet, although there are some levels of noise during the evening."
    elif month == "October":
       formatted_content = "In October, the nights are not as quite as the other months. Higher levels of noise are noticed during the night-times as well. Noise tends to continue throughout the nights. From late Thursday nights to early mornings of Friday the noise continues. The noisiest time of the month is Friday around 08h00. The late Sunday nights and early Monday mornings were the only very quite times of the month."
    elif month == "November":
        formatted_content = "In November, like October, less silent nights were observed. High noise-levels were recorded in the late night Thursdays and early morning of Fridays. The Sunday evenings were also quite noisy. The noisiest time of the month was on Mondays around 08h00."
    elif month == "December":
        formatted_content = "In December, the nights are generally very quite. The noisiest time of the month was Fridays around 12h00. During the weekdays the noise continues till midnight before it fades away. The weekends are also very quite with the exception of Sunday evening for an hour or two."
    else:
        formatted_content = "Throughout the year, it is noticed that the main noise begins during 08h00 of every day and it gradually fades away as the day progresses. The noisiest time of the year was Fridays around 10h00. The weekends were comparatively silent than the other days of the week."

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
        height=580,
    )

    # Update layout for the donut chart
    donut_fig.update_layout(
        title='Event Frequency for ' + (month if month is not None else 'Year'),
        height=400,
        width=500
    )

    # Update layout for the heatmap 
    heatmap_fig.update_layout(
        xaxis_title='Day of the Week',
        yaxis_title='Time',
        title='Hourly Heatmap for ' + (month if month is not None else 'Year') ,
        height=600,
        width=600,
    )

    # Return the formatted date, formatted average date, line graph, donut chart, and heatmap graph
    return formatted_content, formatted_date, formatted_date_avg, fig, donut_fig, heatmap_fig