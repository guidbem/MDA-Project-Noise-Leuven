from dash import Dash, dcc, html, Output, Input       # pip install dash
import dash_bootstrap_components as dbc               # pip install dash-bootstrap-components
import plotly.express as px                     # pip install pandas; pip install plotly express
import dash


dash.register_page(__name__, path='/')




card_main = dbc.Card(
    [        dbc.CardBody(
            [
                html.H2("When is the most quiet moment to take a nap in the Naamsestraat street?", className="card-title",style={"color": "#54B4D3", "paddingTop": "50px", "textAlign": "left","fontSize": "32px"}),
                html.P(
                    "Taking some time off from studying is crucial for students. However, if you reside on Naamsestraat, finding a peaceful moment or being able to take a nap can be challenging due to the street's high level of activity and noise. Are you in search of a solution to identify periods of tranquility during the week? This tool can assist you in pinpointing those moments of calm on Naamsestraat.",
                    className="card-text",
                     style={
        "paddingTop": "20px",  # Add spacing at the top
        "paddingBottom": "50px",  # Add spacing at the bottom
        "textAlign": "left"
    }
                ),
               
            ]
        ),
    ],
    color="dark",   
    inverse=False,   # change color of text (black or white)
    outline=True,  # True = remove the block colors from the background and header
)

card_question = dbc.Card(
    [
    
        dbc.CardBody([
            html.H2("Which is the loudest month at Naamsestraat?", className="card-title"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("A. March"),
                    dbc.ListGroupItem("B. July"),
                    dbc.ListGroupItem("C. August"),
                ], flush=True)
        ]),
    ], color="info",
)

card_text = dbc.Card(
    dbc.CardBody([
        html.H2(
            "The points that seem to be more loud are the ones that are closer to the"
        ),
        html.H1("Oude Markt", className="card-title",style={"color": "#54B4D3", "paddingTop": "50px", "textAlign": "center","fontSize": "64px"}),

    ])
)
       


card_pic = dbc.Card(
    [
        dbc.CardImg(src="data:image/jpeg;base64,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",top=True, bottom=False, className="mx-auto", style={'height': '200px','width': '40%'}),
        dbc.CardBody([
            html.H4("Most noise events registered were related to "),
            html.H1("traffic",className="text-center",style={"color": "#54B4D3"})
        ])
        
    ]
)

card_eff = dbc.Card(
    [
       # dbc.CardImg(src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQavKjlo6x9uDtaE9zs9e0xEL9eFoN7Cgp8hw&usqp=CAU", #class_name="img-fluid img-thumbnail",top=True, bottom=False),
        dbc.CardBody([
            html.H4("Noise negative effects",style={"color": "#54B4D3"}),
            html.P("1. Sleep disturbances:",className="text-center"),
            html.P("2. Stress and psychological effect",className="text-center"),
            html.P("3. Cardiovascular effects",className="text-center"),
            html.P("4. Impaired cognitive performance",className="text-center"),
        ])
        
    ]
)

card_ben = dbc.Card(
    [
       #dbc.CardImg(src="https://encrypted-tbn0.gstatic.com/images?#q=tbn:ANd9GcQDJrxrdoitdYDO644nY4xjj_96Yamjfis9wbCTtXJOgMDQemDHfga8517MyXZAJpSWR2g&usqp=CAU", class_name="img-fluid #img-thumbnail",top=True, bottom=False),
        dbc.CardBody([
            html.H4("Benefits of napping",style={"color": "#54B4D3"}),
            html.P("1. Increased alertness and productivity",className="text-center"),
            html.P("2. Enhanced mood and relaxation",className="text-center"),
            html.P("3. Memory and learning improvement",className="text-center"),
            html.P("4. Stress reduction and health benefits",className="text-center"),
        ])
        
    ]
)

card_pro = dbc.Card(
    [
       #dbc.CardImg(src="https://encrypted-tbn0.gstatic.com/images?#q=tbn:ANd9GcQDJrxrdoitdYDO644nY4xjj_96Yamjfis9wbCTtXJOgMDQemDHfga8517MyXZAJpSWR2g&usqp=CAU", class_name="img-fluid #img-thumbnail",top=True, bottom=False),
        dbc.CardBody([
            html.H4("Noise in Leuven",style={"color": "#54B4D3"}),
            html.P("Monday is the quietest day",className="text-center"),
            html.P("Warm weather increases noise in Naamsestraat",className="text-center"),
            html.P("July is a quiet month",className="text-center"),
            html.P("Places far from the oude markt are calmer",className="text-center"),
        ])
        
    ]
)





layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H1(
                                "Noise in Leuven",
                                className='text-sm-left',
                                style={
                                    "color": "#54B4D3",  # Change to a contrasting color
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
                        src="https://studyabroad.nd.edu/assets/441023/800x333/leuven.jpg",
                        bottom=True,
                        class_name="card-img-overlay h-100 d-flex flex-column justify-content-end",
                        style={"webkitMaskImage": "linear-gradient(to top, transparent 30%, black 100%)",
                               "maskImage": "linear-gradient(to top, transparent 30%, black 100%)",
                               "opacity": 1.0}
                    ),
                ]
            )
        ], width={'size': 12, 'offset': 0})
    ], align="center"),

   
    dbc.Row([
           dbc.Col([
            dbc.Card(
                [
                   dbc.CardBody([
            html.H1(" "),
            html.H1(" "),
            html.H1(" "),
            html.H1(" "),
            html.H1(" "),
            html.H2("")
        ])
                ],
                
            )
        ], width={'size':12, 'offset':0},
           
        )
    ], align="center"),  # Vertical: start, center, end


    dbc.Row([dbc.Col(card_main, width=6),
             dbc.Col(card_question, width=2),
             dbc.Col(card_pic, width=4)], justify="center"),  # justify="start", "center", "end", "between", "around"
  dbc.Row([
           dbc.Col([
            dbc.Card(
                [
                   dbc.CardBody([
            html.H1(" "),
            html.H1(" "),
            html.H1(" "),
            html.H1(" "),
            html.H1(" "),
            html.H2("") 
        ])
                ],
                
            )
        ], width={'size':12, 'offset':0},
           
        )
    ], align="center"),  # Vertical: start, center, end
               dbc.Row(
        dbc.Col(html.H1("",
                        className='text-sm-left'),
                width=18)
    ),
    dbc.Row([
           dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        html.P(
                            "",
                            className="card-text")
                    ),
                    dbc.CardImg(
                        src="https://upload.wikimedia.org/wikipedia/commons/7/7a/Map_Leuven.jpg",
                        bottom=True),
                ],
                
            )
        ], width={'size':12, 'offset':0},
           
        )
    ], align="center"),  # Vertical: start, center, end
        dbc.Row([
           dbc.Col([
            dbc.Card(
                [
                   dbc.CardBody([
            html.H1(" "),
            html.H1(" "),
            html.H1(" "),
             html.H1(" "),
              html.H1(" "),
            html.H2("")
        ])
                ],
                
            )
        ], width={'size':12, 'offset':0},
           
        )
    ], align="center"),  # Vertical: start, center, end
  
               
            dbc.Row([dbc.Col
                     (dbc.CardGroup([card_eff,card_ben, card_pro]))])
    
])
     


