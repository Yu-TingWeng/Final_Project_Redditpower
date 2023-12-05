"""
Display Sentiment Analysis

"""

import dash
from dash import html, register_page, get_asset_url, dash_table

import sys
sys.path.append(r'C:/Users/user/Documents/GitHub/Final_Project_Redditpower')
from sentiment_analysis import df_mean_compound 


dash.register_page(__name__, path="/analysis_dataviz")  # Provide a unique path for the page



layout = html.Div([
    html.H2("1. Word Cloud", style={'color': "#0C2D48", 'font-weight': 'bold'}),
    html.Div("Add Some Descriptions"),
    html.Div([
       html.Img(src=dash.get_asset_url("wordcloud_fomc.png"), style={'width': '50%'}),
       html.Img(src=dash.get_asset_url("wordcloud_reddit.png"), style={'width': '50%'}),
   ], style={'display': 'flex'}),
    
    html.Br(),
    
    html.Div([
       html.H2("2. Aggregate Sentiment Scores", style={'color': "#0C2D48", 'font-weight': 'bold'}),
       html.Div("Add Some Descriptions"),
       dash_table.DataTable(
           id='table',
           columns=[{'name': col, 'id': col} for col in df_mean_compound.columns],
           data=df_mean_compound.to_dict('records'),
       ),
   ]),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.H2("3. Histogram of Compound Scores", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div("Add Some Descriptions"),
        html.Div([
           html.Img(src=dash.get_asset_url("fomc_sentiment_histogram.png"), style={'width': '50%'}),  # Replace with actual histogram image
           html.Img(src=dash.get_asset_url("reddit_sentiment_histogram.png"), style={'width': '50%'}),  # Replace with actual histogram image
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.Div([
        html.H2("4. Time Series Analysis", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div("Add Some Descriptions"),
        html.Div([
           html.Img(src=dash.get_asset_url("fomc_sentiment_time_series.png"), style={'width': '50%'}),  # Replace with actual histogram image
           html.Img(src=dash.get_asset_url("reddit_sentiment_time_series.png"), style={'width': '50%'}),  # Replace with actual histogram image
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.Div([
        html.H2("5. TOP20 Unigrams and Bigrams by Frequency", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.Div("Add Some Descriptions"),
        html.Div([
           html.Img(src=dash.get_asset_url("top_bigrams_fomc.png"), style={'width': '50%'}),  # Replace with actual histogram image
           html.Img(src=dash.get_asset_url("top_bigrams_reddit.png"), style={'width': '50%'}),  # Replace with actual histogram image
       ], style={'display': 'flex'}),
   ]),
    html.Br(),
    html.Br(),
])

