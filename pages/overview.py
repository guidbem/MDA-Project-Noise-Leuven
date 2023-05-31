from dash import Dash, dcc, html,callback, Output, Input       # pip install dash
import dash_bootstrap_components as dbc               # pip install dash-bootstrap-components
import plotly.express as px                     # pip install pandas; pip install plotly express
import dash
import folium
from folium.plugins import FastMarkerCluster
import pandas as pd


dash.register_page(__name__, path='/')


###Construct a map to show where the noise events where registered in the Naamsestraat
# Load the data
df = pd.read_csv('doughnut_data.csv')

# Make a dictionary with Latitude and longitude
locations = {
    '#object_id': [255439, 255444, 255442, 255443, 255441, 255440, 280324],
    'latitude': [50.87723694791674, 50.87394683548034, 50.87452221086784, 50.874206694437916,
                 50.87599947973591, 50.87660565869506, 50.878814448410864],
    'longitude': [4.700756283424897, 4.700096339249199, 4.699913884931272, 4.700066041094888,
                  4.700245812259932, 4.7006594527440955, 4.70085691226008]
}

# Convert to dataframe
locations_df = pd.DataFrame(locations)

# Merge to add latitude and longitude to original dataset
df = pd.merge(df, locations_df, on='#object_id', how='left')

# Make list with latitude and longitude
lats = df['latitude'].tolist()
lons = df['longitude'].tolist()
#Make a locations list containing tuples representing the coordinates on the map.
locations = list(zip(lats, lons))

#Create folium map
map1 = folium.Map(location=[50.878814448410864, 4.70085691226008], zoom_start=25.5)
FastMarkerCluster(data=locations).add_to(map1)



###Create multiple cards with information and specific layouts

card_main = dbc.Card(
    [        dbc.CardBody(
            [
                html.H2("When is the most quiet moment to take a nap in the Naamsestraat street?", className="card-title",style={"color": "#dc3545", "paddingTop": "50px", "textAlign": "left","fontSize": "32px"}),
                html.P(
                    "Taking some time off from studying is crucial for students. However, if you reside on Naamsestraat, finding a peaceful moment or being able to take a nap can be challenging due to the street's high level of activity and noise. Are you in search of a solution to identify periods of tranquility during the week? This tool can assist you in pinpointing those moments of calm on Naamsestraat.",
                    className="card-text",
                      style={
                        "paddingTop": "20px",  # Add spacing at the top
                        "paddingBottom": "50px",  # Add spacing at the bottom
                        "textAlign": "left",
                        "margin": "0",
                        "fontSize": "18px"  # Increase font size
                    }
                ),
               
            ]
        ),
    ],

      outline=False
)

###Create button group
button_group = dbc.ButtonGroup(
    [
        dbc.Button("A.  March", id="button-march", style={"width": "200px"}),
        dbc.Button("B.   July", id="button-july", style={"width": "200px"}),
        dbc.Button("C. August", id="button-august", style={"width": "200px"}),
    ],
    vertical=True,
)

card_question = dbc.Card(
    [
    
        dbc.CardBody([
            html.H2("Which is the loudest month at Naamsestraat?", className="card-title"),
            button_group,
                  ]),
    ], color="lightblue",
)

card_text = dbc.Card(
    dbc.CardBody([
        html.H2(
            "The points that seem to be more loud are the ones that are closer to the"
        ),
        html.H1("Oude Markt", className="card-title",style={"color": "#dc3545", "paddingTop": "50px", "textAlign": "center","fontSize": "64px"}),

    ])
)
       


card_pic = dbc.Card(
    [
        dbc.CardImg(src="assets/traffic.jpg",top=True, bottom=False, className="mx-auto", style={'height': '150px','width': '35%'}),
        dbc.CardBody([
            html.H4("Most noise events registered were related to "),
            html.H1("Traffic",className="text-center",style={"color": "#dc3545","fontSize": "58px"})
        ])
        
    ],
     outline=False
)


card_eff = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Noise negative effects",style={"color": "#dc3545", "paddingTop": "20px", "fontWeight": "bold","textAlign": "center","fontSize": "28px"}),
            html.P("1. Sleep disturbances:",className="text-center"),
            html.P("2. Stress and psychological effect",className="text-center"),
            html.P("3. Cardiovascular effects",className="text-center"),
            html.P("4. Impaired cognitive performance",className="text-center"),
             ],
            className="card-body",
        style={
                "background-image": "url('assets/note.jpg')",
                "background-size": "70%",
                "background-position": "center",
                "background-repeat": "no-repeat",
                "background-color": "rgba(255, 255, 255, 0.001)",  # Adjust the alpha value (0.5 for 50% opacity)
                "padding": "20px",
                "fontSize": "14px",
            },
        ),
    ],
    className="card",
)


card_ben = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Benefits of napping",style={"color": "#dc3545", "paddingTop": "20px", "fontWeight": "bold","textAlign": "center","fontSize": "28px"}),
            html.P("1. Increased alertness and productivity",className="text-center"),
            html.P("2. Enhanced mood and relaxation",className="text-center"),
            html.P("3. Memory and learning improvement",className="text-center"),
            html.P("4. Stress reduction and health benefits",className="text-center"),
             ],
            className="card-body",
     style={
                "background-image": "url('assets/note.jpg')",
                "background-size": "70%",
                "background-position": "center",
                "background-repeat": "no-repeat",
                "background-color": "rgba(255, 255, 255, 0.001)",  # Adjust the alpha value (0.5 for 50% opacity)
                "padding": "20px",
                "fontSize": "14px",
            },
        ),
    ],
    className="card",
)

card_pro = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Noise in Leuven", style={"color": "#dc3545", "paddingTop": "20px", "fontWeight": "bold","textAlign": "center", "fontSize": "28px"}),
                html.P("Weekends are more quiet", className="text-center"),
                html.P("Weather seems to have an effect", className="text-center"),
                html.P("October is a loud month", className="text-center"),
                html.P("Places far from the oude markt are calmer", className="text-center"),
            ],
            className="card-body",
            style={
                "background-image": "url('assets/note.jpg')",
                "background-size": "70%",
                "background-position": "center",
                "background-repeat": "no-repeat",
                "background-color": "rgba(255, 255, 255, 0.001)",  # Adjust the alpha value (0.5 for 50% opacity)
                "padding": "20px",
                "fontSize": "14px",
            },
        ),
    ],
    className="card",
)

card_leuv= dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H1(
                                "Noise in Leuven",
                                className='text-sm-left',
                                style={
                                    "color": "#dc3545",  # Change to a contrasting color
                                    "fontWeight": "bold",
                                    "fontSize": "72px",  # Increase font size
                                    "opacity": 1.0  # Increase opacity
                                }
                            ),
                            html.P(
                                "The City of Leuven in Belgium is trying to strike the balance between a vibrant nightlife and people getting a good night’s sleep. Between August 2021 and November 2022, the city mapped the noise nuisance with seven noise meters between the Collegeberg and the Stuk arts center.",
                                className="card-text",
                                style={
                                    "fontSize": "20px",  # Increase font size
                                    "opacity": 1.0  # Increase opacity
                                }
                            ),
                            html.P(
                                "Peak noises of 70 decibels or more have been registered, between 11 pm and 5 am. The project revealed high night noise levels, particularly on Thursday nights, with average peaks of 88 decibels on Wednesdays and Thursdays. The start of the academic year in October 2022 and the lifting of COVID-19 measures in March 2022 were the noisiest periods, with over 1,000 night noise peaks registered.",
                                className="card-text",
                                style={
                                    "fontSize": "20px",  # Increase font size
                                    "opacity": 1.0  # Increase opacity
                                }
                            )
                        ],
                        style={"paddingTop": "250px", "textAlign": "left"}
                    ),
                    dbc.CardImg(
                        src="assets/leuven.jpg",
                        bottom=True,
                        class_name="card-img-overlay h-100 d-flex flex-column justify-content-end",
                        style={"webkitMaskImage": "linear-gradient(to top, transparent 30%, black 100%)",
                               "maskImage": "linear-gradient(to top, transparent 30%, black 100%)",
                               "opacity": 1.0}
                    ),
                ]
            )



### Create the specific layout as it will be shown in the page

layout = html.Div([
    html.Div(children=[
           # Horizontal line
        html.Div( style={"position": "absolute", "left": "0", "top": "68px", "width": "100%", "height": "2px", "backgroundColor": "lightgray", "zIndex": "0"}),

    ]),



dbc.Row(dbc.Col(card_leuv, width=12, style={"marginTop": "5px"})),

dbc.Row(
    [
        dbc.Col(card_main, width=8),
        dbc.Col(card_question, width=2),
        dbc.Col(card_pic, width=2),
    ],
    className="my-4",
    justify="center",
),


               dbc.Row(
        dbc.Col(html.H1("Registered Noise events on Naamsestraat",
                        className='text-sm-left',
                                style={
                                    "color": "#dc3545",  # Change to a contrasting color
                                    "fontWeight": "bold",
                                    "fontSize": "48px",  # Increase font size
                                    "opacity": 1.0  # Increase opacity
                                }
                                )
    ),
               ),
               
    dbc.Row([
         
         # Add the map here
    html.Div(
        children=[
            html.Iframe(
                id="map",
                srcDoc=map1._repr_html_(),
                style={"width": "100%", "height": "600px", "border": "none"},
            )
        ],
        className="container",
        style={"paddingTop": "50px", "textAlign": "center"},
    )
    
    ], align="center",className="my-5",),  # Vertical: start, center, end
 
  
               
            dbc.Row([dbc.Col
                     (dbc.CardGroup([card_eff,card_ben,card_pro]))])
    
],className="my-4")
     

###callback function  to update the colors of the buttons based on the button that was clicked. 
@callback(
    Output("button-march", "color"),
    Output("button-july", "color"),
    Output("button-august", "color"),
    Input("button-march", "n_clicks"),
    Input("button-july", "n_clicks"),
    Input("button-august", "n_clicks"),
)
def update_button_colors(n_clicks_march, n_clicks_july, n_clicks_august):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "button-july" in changed_id:
        return "primary", "danger", "primary"
    elif "button-march" in changed_id:
        return "success", "primary", "primary"
    elif "button-august" in changed_id:
        return "primary", "primary", "danger"
    else:
        return "primary","primary","primary"