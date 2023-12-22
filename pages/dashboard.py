'''
This file contains the dashboard page.
'''
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os


dash.register_page(__name__, path='/')


# Import Data
path = r"C:\Users\user\Documents\GitHub\Final_Project_Redditpower"

df_fomc = pd.read_excel(os.path.join(path, "FOMC sentiment analysis scores.xlsx"))
df_reddit = pd.read_excel(os.path.join(path, "Reddit sentiment analysis scores.xlsx"))

# Rename 'Date' column to 'date'
df_fomc = df_fomc.rename(columns={'Date': 'date'})
df_reddit = df_reddit.rename(columns={'created_at': 'date'})

# Combine the two dataframes
df_fomc['Source'] = 'FOMC Statement'
df_reddit['Source'] = 'Reddit Posts'
data = pd.concat([df_fomc, df_reddit])

# Prepare some strings
project_purpose = "This project seeks to explore the relationship between the sentiment espoused on the popular internet forum, \
           Reddit’s r/Wallstreetbets subreddit, and the stock market (as a proxy for US economy), and compare it to that of \
           the Federal Open Market Committee (FOMC) statements, one year from start of the latest interest rate hike cycle in March 2022. \
           Known for risky stock bets, edgy humor, and viral popularity during the COVID-19 Pandemic, we wanted to know whether the Redditors \
           on r/Wallstreetbets have an accurate gauge of the macroeconomy – is it a Hitchhiker’s Guide to the moon, or to the ground?"

# Prepare some functions
def filter_data(data, selected_sentiments, selected_sources):
    # Filter based on selected sentiments and sources
    mask_sentiment = data['sentiment'].isin(selected_sentiments)
    mask_source = data['Source'].isin(selected_sources)
    
    # Apply filters
    filtered_data = data[mask_sentiment & mask_source]
    
    return filtered_data

def barplot_sentiment(data):
    # Group by 'Sentiment' and count occurrences
    counts = data.groupby('sentiment').size().reset_index(name='Count')
    fig = px.bar(counts, x='sentiment', y='Count', color='sentiment',
                 labels={'Count': 'Number of Posts'}, title='Number of Posts by Sentiments',)
    return fig

def line_numpost(data):
    # Count the occurrences of each sentiment for each date
    counts = data.groupby(['date', 'sentiment']).size().reset_index(name='Frequency')
    fig = px.line(counts, x='date', y='Frequency', color='sentiment',
                  labels={'Frequency': 'Number of Posts'}, title='Number of Posts by Sentiments and Date',)
    return fig


# Dropdowns Menu
dropdown_sentiment = dbc.Card([
    html.Div([
        # sentiment dropdown label
        html.P('Filter by Sentiment:',
               style={'margin-top': '20px', 'margin-bottom': '0px', 'padding-bottom': '0px'}),
        dcc.Dropdown(
            id='sentiment_dropdown',
            options=[{'label': sentiment, 'value': sentiment} for sentiment in ['positive', 'negative', 'neutral']],
            multi=True,
            value=['positive', 'negative', 'neutral']
        ),

        # source dropdown label
        html.P('Filter by the Source:',
               style={'margin-top': '20px', 'margin-bottom': '0px', 'padding-bottom': '0px'}),
        dcc.Dropdown(
            id='source_dropdown',
            options=[
                {'label': Source, 'value': Source} for Source in ['FOMC Statement', 'Reddit Posts']
            ],
            multi=True,
            value=['FOMC Statement', 'Reddit Posts']
        ),
    ])
], body=True, color='light')



# LAYOUT PAGE
layout = html.Div([
    html.H5(children= project_purpose, style={'color': '#0C2D48', 'line-height': '2'}),
    html.Div([
        # Dropdowns Menu
        dbc.Row([
            dbc.Col(dropdown_sentiment, md=4, style={'margin-top': '20px'}),
        ]),

        # Barplot
        dbc.Row([
            dbc.Col(dcc.Graph(id='line_numpost'), md=6),
            dbc.Col(dcc.Graph(id='bar_sentiment'), md=6),
        ]),
    ]),
])  # End of Layout


# CALLBACKS
@callback(
    [Output('bar_sentiment', 'figure'),
     Output('line_numpost', 'figure')],
    [Input('sentiment_dropdown', 'value'),
     Input('source_dropdown', 'value')]
)
def filtering_data(sentiment, Source):
    '''
    Filter data based on user input
    Input:
        sentiment: list of sentiment
        source: list of source
    Output:
        bar_sentiment: barplot of sentiment
        line_numpost: lineplot of number of posts
    '''
    dff = filter_data(data, sentiment, Source)

    bar_sentiment = barplot_sentiment(dff)
    line_num = line_numpost(dff)

    return bar_sentiment, line_num
