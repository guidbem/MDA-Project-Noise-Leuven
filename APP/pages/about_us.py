import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html, dcc

dash.register_page(__name__, path='/about_us')


# Define the layout
layout = html.Div(
    style={
        "margin": "20px",
        "font-family": "Arial, sans-serif",
        "position": "relative",
        "padding": "20px",
    },
    children=[
        html.Div(
            style={
                "position": "absolute",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "background-image": "url('/assets/leuven_10416_xl.jpg')",  # Update with the correct path or URL
                "background-size": "cover",
                "background-position": "center",
                "background-repeat": "no-repeat",
                "overflow": "hidden",
                "opacity": 0.7,  # Adjust the opacity value as needed (0.5 = 50% opacity)
                "z-index": -1,
            }
        ),
        html.Div(
            style={
                "position": "relative",
                "background-color": "rgba(255, 255, 255, 0.75)",  # Adjust the opacity value as needed (0.7 = 70% opacity)
                "padding": "20px",
            },
            children=[
                html.H1(
                    children="About Us",
                    style={"text-align": "center", "margin-bottom": "50px", "color": "#dc3545"}
                ),
                html.H3(
                    children="Our Objective",
                    style={"text-align": "center"}
                ),
                html.P(
                    "Our primary objective is to examine the correlation between noise levels and various meteorological factors, such as temperature, humidity, wind speed, and precipitation. "
                    "We believe that understanding this relationship will not only shed light on the impact of weather on noise pollution but also provide valuable insights for urban planning, noise mitigation strategies, and enhancing the overall well-being of residents.",
                    style={"text-align": "center"}
                ),
                html.H3(
                    children="Methodology",
                    style={"text-align": "center"}
                ),
                html.P(
                    "To achieve our goal, we used an extensive dataset consisting of noise level measurements from various locations in Leuven (especially in Naamsestraat), along with corresponding meteorological data. "
                    "We employed advanced statistical analysis techniques, including data preprocessing, exploratory data analysis, and machine learning algorithms, to uncover patterns and associations in the data.",
                    style={"text-align": "center"}
                ),
                html.H3(
                    children="App Development with Plotly Dash",
                    style={"text-align": "center"}
                ),
                html.P(
                    "To make our project findings more accessible to the public, we have developed an interactive web application. "
                    "Using Plotly Dash, we have created an intuitive and visually appealing interface that allows users to explore the noise and meteorological data.",
                    style={"text-align": "center"}
                ),
                html.H3(
                    children="Our Team",
                    style={"text-align": "center"}
                ),
                html.P(
                    "Our team is composed of talented individuals from the Master of Statistics and Data Science program, with diverse backgrounds and expertise in statistics, data science, and programming. "
                    "We have worked closely together, utilizing our skills and knowledge to create a strong and insightful project.",
                    style={"text-align": "center"}
                ),
                html.Ul(
                    [
                        html.Li("Ana Sofia Mendes - r0925549"),
                        html.Li("Federico Soldati - r0924528"),
                        html.Li("Guilherme Consul Soares de Bem - r0917829"),
                        html.Li("Ishika Jain - r0915387"),
                        html.Li("Michelle Hernandez - "),
                        html.Li("Sounak Ghosh - r0914328 ")
                    ],
                    style={"text-align": "center", "margin-bottom": "70px"}
                ),
                html.P(
                    "Thank you for visiting our project's webpage. We hope you find our work informative and insightful!",
                    style={"text-align": "center"}
                ),
            ],
        ),
    ],
)