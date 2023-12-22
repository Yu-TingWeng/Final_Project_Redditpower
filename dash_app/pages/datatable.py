'''
Page for the datatable
This page is used to display the data in a table format
'''
import dash
from dash import html, register_page, dash_table, dcc, callback, Output, Input
import pandas as pd


dash.register_page(__name__)


# Import FOMC Data
df_fomc = pd.read_excel(r"C:\Users\user\Documents\GitHub\final-project-redditpower\Data\scraped_fomc_data.xlsx")
df_fomc = df_fomc[df_fomc['Title'].str.contains('FOMC statement')]

# Import Reddit Data
df_reddit = pd.read_excel(r"C:\Users\user\Documents\GitHub\final-project-redditpower\Data\scraped_reddit_data.xlsx")
df_reddit['created_at'] = pd.to_datetime(df_reddit['created_at'])
start_date = '2022-03-01'
end_date = '2023-03-31'
df_reddit = df_reddit[(df_reddit['created_at'] >= start_date) & (df_reddit['created_at'] <= end_date)]
df_reddit = df_reddit[["created_at", "id_str", "subreddit", "title", "selftext", "upvote_ratio", "permalink", "num_comments"]]


# LAYOUT PAGE
layout = html.Div([
    html.Div([
        "Select FOMC Statement or Reddit Posts: ",
        dcc.RadioItems(
            options=['FOMC Statement', 'Reddit Posts'],
            value='FOMC Statement',
            id='analytics-input'
        )
    ]),
    html.Br(),
    html.Div(id='analytics-output'),
])

# CALLBACKS
@callback(
    Output('analytics-output', 'children'),
    [Input('analytics-input', 'value')]
)
def update_output(selected_option):
    if selected_option == 'FOMC Statement':
        # Display FOMC DataFrame
        return dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in df_fomc.columns],
            data=df_fomc.to_dict('records'),
            page_current=0,
            page_size=5,
            page_action='native',
            style_cell={'textAlign': 'left'},
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            style_table={'overflowX': 'auto'}
        )
    elif selected_option == 'Reddit Posts':
        # Display Reddit DataFrame
        return dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in df_reddit.columns],
            data=df_reddit.to_dict('records'),
            page_current=0,
            page_size=5,
            page_action='native',
            style_cell={'textAlign': 'left'},
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            style_table={'overflowX': 'auto'}
        )
    else:
        return "Invalid selection"
