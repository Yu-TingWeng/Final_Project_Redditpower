'''
This is the main script for the dashboard. It will be used to create the layout of the dashboard.
This will call pages in the container view.
'''
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
import dash

# Initialize the app
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           use_pages=True)
app.title='final-project-redditpower'
server = app.server

# Navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/", style={'font-weight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Sentiment Analysis and Data Visualization", href="/analysis_dataviz", style={'font-weight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Sentiment Analysis and Stock Price", href="/stocks", style={'font-weight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Raw Data", href="/datatable", style={'font-weight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Text Prediction", href="/prediction", style={'font-weight': 'bold'})),
    ],
    brand_href="/",
    sticky="top",
    color="#0C2D48",
    dark=True,)
    
# LAYOUT PAGE   
app.layout = html.Div([
    dbc.Container([
        html.H1(children='r/Wallstreetbets: A Hitchhiker\'s Guide to the Moon or to the Ground?', style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.H5(children='The University of Chicago, Harris School of Public Policy'),
        html.H5(children='Data and Programming for Public Policy II - Python Programming: Final Project'),
        html.H5(children='Team Members: Andrew Chen, Yuting Weng'),
        html.Br(),
        # Navigation bar
        html.Div(navbar),
        html.Br(),
        dash.page_container
    ])
])

# Run
if __name__ == '__main__':
    app.run(debug=True, port=8051)


# References:
# Dash: https://dash.plotly.com/tutorial
# Use Pages: https://dash.plotly.com/urls
# Navs: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/nav/
# Deploying a Dash Application on Render: https://github.com/thusharabandara/dash-app-render-deployment
# ColorHexa: https://www.colorhexa.com/a9a9a2
