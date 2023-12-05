from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
import dash



app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           use_pages=True)
app.title='final-project-redditpower'

server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/", style={'font-weight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Analysis and Data Visualization", href="/analysis_dataviz", style={'font-weight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Data", href="/datatable", style={'font-weight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Text Predictions", href="/prediction", style={'font-weight': 'bold'})),
    ],
    brand_href="/",
    sticky="top",
    color="#0C2D48",
    dark=True,)
    
    
app.layout = html.Div([
    dbc.Container([
        html.H1(children='Data and Programming for Public Policy II - Python Programming'),
        html.H2(children='Final Project: Reddit Power'),
        html.Div(children='Team Members: Andrew Chen, Yuting Weng'),
        html.Div(children='The Purpose of our final project is to...'),
        # Navigation bar
        html.Div(navbar),
        html.Br(),
        dash.page_container
    ])
])


if __name__ == '__main__':
    app.run(debug=True, port=8051)


# References:
# Dash: https://dash.plotly.com/tutorial
# Use Pages: https://dash.plotly.com/urls
# Navs: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/nav/
# Deploying Dash: https://dash.plotly.com/deployment
