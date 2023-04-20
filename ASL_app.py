import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
from user_agents import parse
from flask import request

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SKETCHY, FA])
server = app.server

order = ["About", "Letter quiz", "Word quiz", "Sentence quiz", "Asl decoder competition"]

app.layout = dbc.Container(className="mt-4 mb-4", children=[
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(id='logo'),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Nav(
                                dbc.NavbarToggler(id='navbar-toggler'),
                                className="ml-auto",
                            ),
                            width="auto"
                        ),
                    ],
                    justify="center",  # Add this property to center the image
                    align="center",
                ),
                dbc.Collapse(dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink(page['name'].title(), href=page['path'],
                                                 style={'fontSize': '20px', 'px': '10px', 'py': '8px'},
                                                 className="mx-auto"))
                        
                        for page in sorted(dash.page_registry.values(), key=lambda x: order.index(x['name']))
                    ],
                    navbar=True,
                    className="d-flex justify-content-between flex-grow-1"
                ), id="navbar-collapse", navbar=True),
                # Add fluid class to the container to make it full-width on small devices
            ],
            fluid=True,  # Add this property to make the container full-width on small devices
        ),
        # color="dark",
        # dark=True,
        className="mb-5",
        sticky="top",
        expand="lg"  # Add this attribute to make the navbar responsive
    ),
    dash.page_container
])


@app.callback([Output('logo', 'children'), Output('navbar-collapse', 'is_open')],
              [Input('url', 'pathname'), Input('navbar-toggler', 'n_clicks')],
              [State('navbar-collapse', 'is_open')])
def update_logo_height_and_toggle_navbar_collapse(pathname, n_clicks, is_open):
    user_agent = parse(request.headers['User-Agent'])
    logo_height = "150px" if not user_agent.is_mobile else "100px"
    logo = html.Img(src="assets/Logo.png", height=logo_height)

    ctx = dash.callback_context
    if not ctx.triggered:
        return logo, False
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'url':
            return logo, False
        else:
            if n_clicks is not None:
                return logo, not is_open
            return logo, is_open


if __name__ == '__main__':
    app.run_server(debug=True)