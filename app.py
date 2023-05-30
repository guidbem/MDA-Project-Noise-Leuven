from dash import Dash, dcc, html, callback, Output, Input,callback_context  
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
            id="overview-link",
        ),
        dcc.Link(
            "Analysis 1",
            href="/analysis-1",
            className="link",
            style={"margin-right": "20px"},
            id="analysis-1-link",
        ),
        dcc.Link(
            "Analysis 2",
            href="/analysis-2",
            className="link",
            style={"margin-right": "20px"},
            id="analysis-2-link",
        ),
        dcc.Link(
            "Model",
            href="/model",
            className="link",
            style={"margin-right": "0px"},
            id="model-link",
        ),
        dcc.Link(
            "About Us",
            href="/about_us",
            className="link",
            id="about-us-link",
        ),
    ],
    style={
        "background-color": "white",  # change color accodingly
        "height": "70px",
        "display": "flex",
        "align-items": "center",
        "margin-left": "500px",  
        "margin-right": "500px",  
        "justify-content": "space-between",
        "background-repeat": "no-repeat",
        "background-size": "cover",
    },
)


app.layout = html.Div(
    [   
        html.Link(
            rel="stylesheet",
            href="/assets/styles.css"  # Path to the CSS file
        ),
        dcc.Location(id="url", refresh=False),
        nav_bar,
        dash.page_container
    ]
)


@app.callback(
    [dash.dependencies.Output(f"{link_id}", "className") for link_id in ["overview-link", "analysis-1-link", "analysis-2-link", "model-link", "about-us-link"]],
    [dash.dependencies.Input("url", "pathname")]
)
def update_active_link(pathname):
    return ["link active" if f"/{link_id.replace('-link', '')}" == pathname or link_id == "overview-link" and pathname == "/" else "link" for link_id in ["overview-link", "analysis-1-link", "analysis-2-link", "model-link", "about_us-link"]]

if __name__ == '__main__':
    app.run_server(debug=True)
