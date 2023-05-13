import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
from dash.dependencies import Input, Output

# Sample data for the doughnut chart
labels = ['Category A', 'Category B', 'Category C']
values = [30, 50, 20]

# Months for the slider
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1('Doughnut Chart and Heatmap Dashboard'),
        dcc.Graph(
            id='doughnut-chart'
        ),
        dcc.Graph(
            id='heatmap',
            style={'height': '600px', 'width': '600px'}  # Adjust the height and width of the heatmap
        ),
        dcc.Slider(
            id='month-slider',
            min=0,
            max=len(months) - 1,
            value=0,
            marks={i: months[i] for i in range(len(months))},
            step=None,
            tooltip={'placement': 'bottom'}
        )
    ]
)

# Callback function to update the doughnut chart and rotation angle
@app.callback(
    Output('doughnut-chart', 'figure'),
    [Input('month-slider', 'value')]
)
def update_chart(selected_month):
    # Get data for the selected month
    month_data = get_month_data(selected_month)  # Replace this with your data retrieval logic

    # Calculate rotation angle based on selected month
    rotation_angle = 360 * selected_month / len(months)

    # Create the doughnut chart figure
    figure = go.Figure(
        data=[go.Pie(labels=labels, values=month_data, hole=0.5, rotation=rotation_angle)],
        layout=go.Layout(title='Doughnut Chart')
    )

    return figure

# Callback function to update the heatmap
@app.callback(
    Output('heatmap', 'figure'),
    [Input('month-slider', 'value')]
)
def update_heatmap(selected_month):
    # Get data for the selected month
    month_data = get_month_data(selected_month)  # Replace this with your data retrieval logic

    # Generate random data for the heatmap
    # Replace this with your actual data retrieval and processing logic
    random_data = np.random.randint(low=0, high=100, size=(24, 7))

    # Create the heatmap figure
    figure = ff.create_annotated_heatmap(
        z=random_data,
        x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        y=[f'{hour}:00' for hour in range(24)],
        colorscale='Viridis',
        showscale=True,
        annotation_text=random_data.tolist(),
        hoverinfo='z'
    )

    figure.update_layout(title='Heatmap')

    return figure

# Replace this function with your own data retrieval logic ###
def get_month_data(selected_month):
    # Return data for the selected month
    # Replace this with your data retrieval logic
    # Example: return [30, 50, 20] for each month
    return [30, 50, 20]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)