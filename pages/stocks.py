'''
Display the correlation between FOMC Statement, Reddit, and Stock Prices
'''
import dash
from dash import html, register_page, get_asset_url, dash_table
from sentiment_analysis import df_mean_compound 


dash.register_page(__name__) 

# LAYOUT PAGE
layout = html.Div([
    html.H2("1. S&P 500", style={'color': "#0C2D48", 'font-weight': 'bold'}),
    html.Div("Add Some Descriptions"),
    html.Div([
       html.Img(src=dash.get_asset_url("FOMC-SP500.png"), style={'width': '50%'}),
       html.Img(src=dash.get_asset_url("Reddit_SP500.png"), style={'width': '50%'}),
   ], style={'display': 'flex'}),
    
    html.Br(),
    
    html.Div([
        html.H2("2. Dow Jones Industrial Average index", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div("Add Some Descriptions"),
        html.Div([
           html.Img(src=dash.get_asset_url("FOMC-DJ.png"), style={'width': '50%'}), 
           html.Img(src=dash.get_asset_url("Reddit-DJ.png"), style={'width': '50%'}),  
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.Div([
        html.H2("3. NASDAQ Composite", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div("Add Some Descriptions"),
        html.Div([
           html.Img(src=dash.get_asset_url("FOMC-NASDAQ.png"), style={'width': '50%'}),  
           html.Img(src=dash.get_asset_url("Reddit-NASDAQ.png"), style={'width': '50%'}),  
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    html.Br(),
])

