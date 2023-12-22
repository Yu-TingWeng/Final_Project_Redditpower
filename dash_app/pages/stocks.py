'''
Display the correlation between FOMC Statement, Reddit, and Stock Prices
'''
import dash
from dash import html, register_page, get_asset_url, dash_table
from sentiment_analysis import df_mean_compound
import sys
sys.path.append(r"C:\Users\user\Documents\GitHub\final-project-redditpower")
import Texts as text


dash.register_page(__name__) 

# LAYOUT PAGE
layout = html.Div([
    html.H2("Method and Finding", style={'color': "#0C2D48", 'font-weight': 'bold'}),
    html.H5(text.stock_text, style={'line-height': '2'}),
    html.Br(),
    html.H2("1. S&P 500", style={'color': "#0C2D48", 'font-weight': 'bold'}),
    html.Div([
       html.Img(src=dash.get_asset_url("FOMC-SP500.png"), style={'width': '50%'}),
       html.Img(src=dash.get_asset_url("Reddit_SP500.png"), style={'width': '50%'}),
   ], style={'display': 'flex'}),
    
    html.Br(),
    
    html.Div([
        html.H2("2. Dow Jones Industrial Average index", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div([
           html.Img(src=dash.get_asset_url("FOMC-DJ.png"), style={'width': '50%'}), 
           html.Img(src=dash.get_asset_url("Reddit-DJ.png"), style={'width': '50%'}),  
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.Div([
        html.H2("3. NASDAQ Composite", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div([
           html.Img(src=dash.get_asset_url("FOMC-NASDAQ.png"), style={'width': '50%'}),  
           html.Img(src=dash.get_asset_url("Reddit-NASDAQ.png"), style={'width': '50%'}),  
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.Div([
        html.H2("4. Regression Summary Table", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div([
           html.H5("FOMC-S&P500", style={'width': '45%', 'color': "#0C2D48", 'font-weight': 'bold', 'text-align': 'center'}), 
           html.H5("Reddit-S&P500", style={'width': '45%', 'color': "#0C2D48", 'font-weight': 'bold', 'text-align': 'center'}),  
       ], style={'display': 'flex'}),
        html.Div([
           html.Img(src=dash.get_asset_url("fomc_sp500_stat.png"), 
                    style={'width': '45%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}), 
           html.Img(src=dash.get_asset_url("reddit_sp500_stat.png"), 
                    style={'width': '45%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),  
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.H2("Conclusions", style={'color': "#0C2D48", 'font-weight': 'bold'}),
    html.H5(text.conclusion_text, style={'line-height': '2'}),
    html.Br(),
    html.Br(),
])

