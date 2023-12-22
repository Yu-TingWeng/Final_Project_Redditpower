"""
This is Shiny App
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, ui, reactive, render
import sys
sys.path.append(r"C:\Users\user\Documents\GitHub\Final_Project_Redditpower")
import Texts as text

# Import Data
path = r"C:\Users\user\Documents\GitHub\Final_Project_Redditpower"
df_fomc = pd.read_excel(os.path.join(path, 'FOMC sentiment analysis scores.xlsx'))
df_reddit = pd.read_excel(os.path.join(path, 'Reddit sentiment analysis scores.xlsx'))

# Data Cleaning
# Rename 'Date' column to 'date'
df_fomc = df_fomc.rename(columns={'Date': 'date'})
df_reddit = df_reddit.rename(columns={'created_at': 'date'})

# Unify datetime formats
def timezone_adjust(df, timezone):
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(timezone)
    return df

timezone = 'UTC'
df_fomc = timezone_adjust(df_fomc, timezone)
df_reddit = timezone_adjust(df_reddit, timezone)

# Combine the two dataframes
df_fomc['Source'] = 'FOMC Statement'
df_reddit['Source'] = 'Reddit Posts'
data = pd.concat([df_fomc, df_reddit])

df_reddit.rename(columns={'created_at': 'Date'}, inplace=True)




# Define Shiny app UI
app_ui = ui.page_fluid(
    # Header section
    ui.row(
        ui.column(12, ui.h1('r/Wallstreetbets: A Hitchhiker\'s Guide to the Moon or to the Ground?'), 
                  style='font-weight: bold ; color : #0C2D48'),
        ),
    ui.row(),
    ui.row(
        ui.column(12, ui.h4('PPHA 30538 Data and Programming for Public Policy II- Python Programming- Final Project')),
        ),
    ui.row(
        ui.column(4, ui.h4("Team Members: Andrew Chen, Yuting Weng"), style="height: 60px"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.project_purpose), style="height: 150px"),
        ),

    # Input section
    ui.row(
        ui.column(6, ui.input_selectize(id='sentiment',
                                        label='Choose Sentiments',
                                        choices=['positive', 'negative', 'neutral'],
                                        multiple=True)),
        ui.column(6, ui.input_selectize(id='source',
                                        label='Choose FOMC Statement or Reddit Posts',
                                        choices=['FOMC Statement', 'Reddit Posts'],
                                        multiple=True)),
        ),
    
    # Output section
    ui.row(
        ui.column(6, ui.output_plot('barplot_sentiment')),
        ui.column(6, ui.output_plot('line_numpost')),
        style="height: 500px"
        ),
    ui.row(
        ui.column(12, ui.h2('Sentiment Analysis and Data Visualization'), 
                  style="font-weight: bold ; color : #0C2D48 ; height: 80px"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.introduction_text), style="height: 150px"),
        ),
    
    # Display Word Cloud
    ui.row(
        ui.column(12, ui.h3('1. Word Cloud'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.wordcloud_text), style="height: 100px"),
        ),
    ui.row(
        ui.column(6, ui.output_image('wordcloud_fomc'), style="height: 450px"),
        ui.column(6, ui.output_image('wordcloud_reddit'), style="height: 450px")
        ),
    
    # Display Aggregate Sentiment Scores
    ui.row(
        ui.column(12, ui.h3('2. Aggregate Sentiment Scores'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.aggregate_text), style="height: 100px"),
        ),
    ui.row(
        ui.column(6, ui.output_table('mean_data')),
        ),
    
    # Display Histogram of Compound Scores
    ui.row(
        ui.column(12, ui.h3('3. Histogram of Compound Scores'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.histogram_text), style="height: 100px"),
        ),
    ui.row(
        ui.column(6, ui.output_image('histogram_fomc'), 
                  style="height: 450px"),
        ui.column(6, ui.output_image('histogram_reddit'), 
                  style="height: 450p")
        ),
    
    # Display Time Series Analysis
    ui.row(
        ui.column(12, ui.h3('4. Time Series Analysis'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.time_series_text), style="height: 100px"),
        ),
    ui.row(
        ui.column(6, ui.output_image('time_series_fomc'), 
                  style="height: 450px"),
        ui.column(6, ui.output_image('time_series_reddit'), 
                  style="height: 450p")
        ),
    
    # Display TOP20 Unigrams and Bigrams by Frequency
    ui.row(
        ui.column(12, ui.h3('5. TOP20 Unigrams and Bigrams by Frequency'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.top20_text), style="height: 100px"),
        ),
    ui.row(
        ui.column(6, ui.output_image('top20_fomc'), 
                  style="height: 550px"),
        ui.column(6, ui.output_image('top20_reddit'), 
                  style="height: 550p")
        ),
    ui.row(
        ui.column(12, ui.h2('Sentiment Analysis and Stock Price'), 
                  style="font-weight: bold ; color : #0C2D48 ; height: 80px"),
        ),
    ui.row(
        ui.column(12, ui.h5(text.stock_text), style="height: 150px"),
        ),
    
    # Display the relationships between Stock Prices and FOMC Statement, Reddit Posts
    ui.row(
        ui.column(12, ui.h3('1. S&P 500'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(6, ui.output_image('fomc_sp500'), style="height: 350px"),
        ui.column(6, ui.output_image('reddit_sp500'), style="height: 350px")
        ),
    ui.row(
        ui.column(12, ui.h3('2. Dow Jones Industrial Average index'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(6, ui.output_image('fomc_dj'), style="height: 350px"),
        ui.column(6, ui.output_image('reddit_dj'), style="height: 350px")
        ),
    ui.row(
        ui.column(12, ui.h3('3. NASDAQ Composite'), 
                  style="font-weight: bold ; color : #0C2D48"),
        ),
    ui.row(
        ui.column(6, ui.output_image('fomc_nasdaq'), style="height: 350px"),
        ui.column(6, ui.output_image('reddit_nasdaq'), style="height: 350px")
        ),
    
)


# Define Shiny app server
def server (input, output, session): 
    @render.image 
    def wordcloud_fomc(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\wordcloud_fomc.png", 
                'contentType': 'image/png'}
    @render.image 
    def wordcloud_reddit(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\wordcloud_reddit.png", 
                'contentType': 'image/png'}
    
    @output
    @render.table
    def mean_data():
        df_mean_compound = pd.read_excel(os.path.join(path, 'Mean Compound Scores.xlsx'))
        return df_mean_compound
    
    @render.image 
    def histogram_fomc(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\fomc_sentiment_histogram.png", 
                'contentType': 'image/png'}
    @render.image 
    def histogram_reddit(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\reddit_sentiment_histogram.png", 
                'contentType': 'image/png'}
    
    @render.image 
    def time_series_fomc(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\fomc_sentiment_time_series.png", 
                'contentType': 'image/png'}
    @render.image 
    def time_series_reddit(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\reddit_sentiment_time_series.png", 
                'contentType': 'image/png'}
    
    @render.image 
    def top20_fomc(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\top_bigrams_fomc.png", 
                'contentType': 'image/png'}
    @render.image 
    def top20_reddit(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\top_bigrams_reddit.png", 
                'contentType': 'image/png'}
    
    @render.image 
    def fomc_sp500(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\FOMC-SP500.png", 
                'contentType': 'image/png'}
    @render.image 
    def reddit_sp500(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\Reddit_SP500.png", 
                'contentType': 'image/png'}
    
    @render.image 
    def fomc_dj(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\FOMC-DJ.png", 
                'contentType': 'image/png'}
    @render.image 
    def reddit_dj(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\Reddit-DJ.png", 
                'contentType': 'image/png'}
    
    @render.image 
    def fomc_nasdaq(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\FOMC-NASDAQ.png", 
                'contentType': 'image/png'}
    @render.image 
    def reddit_nasdaq(): 
        return {'src': r"C:\Users\user\Documents\GitHub\final-project-redditpower\assets\FOMC-NASDAQ.png", 
                'contentType': 'image/png'}
    
    @reactive.Calc
    def filter_data():
        # Filter based on selected sentiments and sources
        selected_sentiments = input.sentiment()
        selected_sources = input.source()
        mask_sentiment = data['sentiment'].isin(selected_sentiments)
        mask_source = data['Source'].isin(selected_sources)
        
        # Apply filters
        filtered_data = data[mask_sentiment & mask_source]
        return filtered_data
    
    
    def cal_numpost():
        # Count the occurrences of each sentiment for each date
        filtered_data = filter_data()
        counts = filtered_data.groupby(['date', 'sentiment']).size().reset_index(name='Frequency')
        positive_count= counts[counts['sentiment']=='positive']
        negative_count= counts[counts['sentiment']=='negative']
        neutral_count= counts[counts['sentiment']=='neutral']
        return positive_count, negative_count, neutral_count
    
    @output
    @render.plot
    def barplot_sentiment():
        # Filtered data from the reactive function
        filtered_data = filter_data()
        counts = filtered_data.groupby('sentiment').size().reset_index(name='Count')

        fig, ax = plt.subplots()
        ax.bar(counts['sentiment'], counts['Count'])
        plt.xlabel('Sentiment')
        plt.ylabel('Number of Posts')
        plt.title('Number of Posts by Sentiments')
        return fig
    
    @output
    @render.plot
    def line_numpost():
        positive_count, negative_count, neutral_count = cal_numpost()
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(positive_count['date'], positive_count['Frequency'], label='positive')
        ax.plot(negative_count['date'], negative_count['Frequency'], label='negative')
        ax.plot(neutral_count['date'], neutral_count['Frequency'], label='neutral')
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Posts')
        ax.set_title('Number of Posts by Sentiments and Date')
        ax.legend()
        return ax
    
    
app = App(app_ui, server)


# References:
# Shiny input controls: https://shiny.posit.co/py/docs/inputs.html
# Shiny functions: https://shiny.posit.co/py/api/ui.output_image.html
