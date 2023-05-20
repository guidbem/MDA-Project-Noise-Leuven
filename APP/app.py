from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

nav_bar = html.Nav(
    children=[
        dcc.Link(
            "Overview",
            href="/",
            className="link",
            style={"margin-right": "20px"},
        ),
        dcc.Link(
            "Analysis 1",
            href="/analysis-1",
            className="link",
            style={"margin-right": "20px"},
        ),
        dcc.Link(
            "Analysis 2",
            href="/analysis-2",
            className="link",
            style={"margin-right": "20px"},
        ),
        dcc.Link(
            "Model",
            href="/model",
            className="link",
            style={"margin-right": "0px"},
        ),
        dcc.Link(
            "About Us",
            href="/about_us",
            className="link",
        ),
    ],
    style={
        "background-color": "white",
        "height": "70px",
        "display": "flex",
        "align-items": "center",
        "margin-left": "500px",  
        "margin-right": "500px",  
        "justify-content": "space-between",
    },
)


app.layout = html.Div(
    [   
        html.Link(
            rel="stylesheet",
            href="/assets/styles.css"  # Path to the CSS file
        ),
        nav_bar,
        dash.page_container
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
