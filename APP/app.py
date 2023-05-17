from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash
import dash_vtk


app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

nav_bar = html.Nav(
    children=[
        dcc.Link(
            "Overview",
            href="/",
            className="link",  # Added "link" class
        ),
        dcc.Link(
            "Analysis 1",
            href="/analysis-1",
            className="link",  # Added "link" class
        ),
        dcc.Link(
            "Analysis 2",
            href="/analysis-2",
            className="link",  # Added "link" class
        ),
        dcc.Link(
            "Model",
            href="/model",
            className="link",  # Added "link" class
        ),
        dcc.Link(
            "About Us",
            href="/about_us",
            className="link",  # Added "link" class
        ),
    ],
    style={
        "background-color": "white",
        "height": "70px",
        "width": "35%",
        "display": "flex",
        "align-items": "center",
        "margin-left": "auto",
        "margin-right": "auto",
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
