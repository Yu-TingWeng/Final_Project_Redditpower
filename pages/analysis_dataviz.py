"""
Display Sentiment Analysis

"""
import dash
from dash import html, register_page, get_asset_url, dash_table
from sentiment_analysis import df_mean_compound 


dash.register_page(__name__, path="/analysis_dataviz") 

# Prepare some texts
introduction_text = """
                    The raw data, as shown in the raw data page, undergoes a series of preprocessing steps to optimize its suitability for subsequent analysis. 
                    Stopwords are removed, and lemmatization is applied to reduce words to their base forms. 
                    Subsequently, sentiment analysis is conducted on the preprocessed text utilizing the VADER sentiment analyzer. The compound score is then 
                    utilized to categorize the data into three sentiments: 'positive,' 'neutral,' or 'negative.' 
                    These sentiments serve as key metrics for generating various visualizations.
                    """
wordcloud_text = """
                The word cloud visually represents the most frequently occurring keywords in the statements 
                and posts we extracted. Notably, the FOMC statement features a prevalence of formal policy vocabulary 
                and technical jargon, including terms like monetary policy, federal fund rate, and (rate) target. 
                In contrast, the Reddit posts' word cloud emphasizes topics such as inflation, recession, market, company, 
                and price, which hold more individual-level significance due to their direct impact on personal circumstances.
                """
aggregate_text = """
                  Aggregately, the FOMC statements showing a mean compound score of 0.0972, while Reddit posts has a score of -0.0432, 
                  showing the difference in sentiments among the two data sets.
                  """
histogram_text = """
                  These histograms show the compound sentiment scores for the two data sets. We can see that the sentiments expressed 
                  within FOMC statement are less extreme than Reddit posts.
                  """
time_series_text = """
                    These graphs show the compound scores for both data sets. We can see that the FOMC statements show the lowest 
                    compound sentiment scores between August 2022 and January 2023, while Reddit dipped lowest in May 2022, then 
                    goes on a generally upward trend.
                    """
top20_text = """
              These graphs show the top bigrams by frequency in both data sets. Somewhat similar to the results of the word cloud, 
              we can see that the FOMC statements contain more official and technical jargons, while the Reddit posts hold more words 
              that are relevant to individual daily lives.
              """

# LAYOUT PAGE
layout = html.Div([
    html.H2("Method", style={'color': "#0C2D48", 'font-weight': 'bold'}),
    html.H5(introduction_text, style={'line-height': '2'}),
    html.Br(),
    html.H2("1. Word Cloud", style={'color': "#0C2D48", 'font-weight': 'bold'}),
    html.H5(wordcloud_text, style={'line-height': '2'}),
    html.Div([
       html.Img(src=dash.get_asset_url("wordcloud_fomc.png"), style={'width': '50%'}),
       html.Img(src=dash.get_asset_url("wordcloud_reddit.png"), style={'width': '50%'}),
   ], style={'display': 'flex'}),
    
    html.Br(),
    
    html.Div([
       html.H2("2. Aggregate Sentiment Scores", style={'color': "#0C2D48", 'font-weight': 'bold'}),
       html.H5(aggregate_text, style={'line-height': '2'}),
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
        html.H5(histogram_text, style={'line-height': '2'}),
        html.Div([
           html.Img(src=dash.get_asset_url("fomc_sentiment_histogram.png"), style={'width': '50%'}),  # Replace with actual histogram image
           html.Img(src=dash.get_asset_url("reddit_sentiment_histogram.png"), style={'width': '50%'}),  # Replace with actual histogram image
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.Div([
        html.H2("4. Time Series Analysis", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.H5(time_series_text, style={'line-height': '2'}),
        html.Div([
           html.Img(src=dash.get_asset_url("fomc_sentiment_time_series.png"), style={'width': '50%'}),  # Replace with actual histogram image
           html.Img(src=dash.get_asset_url("reddit_sentiment_time_series.png"), style={'width': '50%'}),  # Replace with actual histogram image
       ], style={'display': 'flex'}),
   ]),
    
    html.Br(),
    
    html.Div([
        html.H2("5. TOP20 Unigrams and Bigrams by Frequency", style={'color': "#0C2D48", 'font-weight': 'bold'}),
        html.H5(top20_text, style={'line-height': '2'}),
        html.Div([
           html.Img(src=dash.get_asset_url("top_bigrams_fomc.png"), style={'width': '50%'}),  # Replace with actual histogram image
           html.Img(src=dash.get_asset_url("top_bigrams_reddit.png"), style={'width': '50%'}),  # Replace with actual histogram image
       ], style={'display': 'flex'}),
   ]),
    html.Br(),
    html.Br(),
])

