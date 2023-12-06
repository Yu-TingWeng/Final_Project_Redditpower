"""
Text Files
"""

project_purpose = "This project seeks to explore the relationship between the sentiment espoused on the popular internet forum, \
           Reddit’s r/Wallstreetbets subreddit, and the stock market (as a proxy for US economy), and compare it to that of \
           the Federal Open Market Committee (FOMC) statements, one year from start of the latest interest rate hike cycle in March 2022. \
           Known for risky stock bets, edgy humor, and viral popularity during the COVID-19 Pandemic, we wanted to know whether the Redditors \
           on r/Wallstreetbets have an accurate gauge of the macroeconomy – is it a Hitchhiker’s Guide to the moon, or to the ground?"

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
stock_text = """
            We plotted the compound sentiments and monthly mean compound sentiments for Reddit posts on top of the major stock indices. 
            We also used OLS to estimate the correlation between the data set sentiments and the closing prices. All the models 
            (FOMC/Reddit on S&P 500/Dow Jones/NASDAQ) are sadly not statistically significant, which is similar to what we expected to 
            see for the Reddit posts. Interestingly, the R-squared from the FOMC-stock indices pairs is higher than that of Reddit-stock 
            indices pairs.
            """
model_text = """
            A sentiment analysis model is constructed using a Support Vector Machine (SVM) classifier. The dataset is divided into training 
            and testing sets, and text data is processed and transformed into numerical features using TF-IDF vectorization. The SVM model, 
            utilizing a radial basis function (RBF) kernel, is trained on the TF-IDF transformed training data and subsequently assessed on the 
            testing set. Despite the initial implementation, the model's accuracy is reported to be around 70%, indicating room for improvement. 
            """
conclusion_text = """
            Similar to our initial expectation, Reddit posts’ correlations with stock closing prices aren’t significant nor large. On the other hand, 
            despite line graphs seemingly showing co-movement between sentiments expressed in FOMC statements and stock closing prices, the relationship 
            seems to be not robust statistically. These could be explained by some of the limitations we describe below. 
            """





