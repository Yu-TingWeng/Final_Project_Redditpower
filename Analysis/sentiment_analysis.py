"""
Sentiment Analysis for FOMC Statement and Reddit Posts
"""
import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


# Import FOMC Data
path = r"C:\Users\user\Documents\GitHub\Final_Project_Redditpower\Data"
df_fomc = pd.read_excel(os.path.join(path, 'scraped_fomc_data.xlsx'))
df_fomc = df_fomc[df_fomc['Title'].str.contains('FOMC statement')]

# Import Reddit Data
df_reddit = pd.read_excel(os.path.join(path,'scraped_reddit_data.xlsx'))
df_reddit['created_at'] = pd.to_datetime(df_reddit['created_at'])
start_date = '2022-03-01'
end_date = '2023-03-31'
df_reddit = df_reddit[(df_reddit['created_at'] >= start_date) & (df_reddit['created_at'] <= end_date)]



# PART I: Preprocessing Data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove links starting with 'http' or 'https'
    text = re.sub(r'http\S+|https\S+', '', text)
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^\w\s\d]', '', text)
    return text

df_reddit['text'] = df_reddit['text'].apply(preprocess_text)

# Remove Stopwords
nltk.download('stopwords')
def remove_stopwords(text):
    """
    Remove stop words from the input text.
    
    Returns:
    - Text after removing stop words.
    """
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in text.split() if word.casefold() not in stop_words]
    filtered_words = [word for word in filtered_words if word.casefold() not in {'x200b','filler'}]
    filtered_text = ' '.join(filtered_words)
    return filtered_text

df_fomc['clean text'] = df_fomc['Linked Content'].apply(remove_stopwords)
df_reddit['clean text'] = df_reddit['text'].apply(remove_stopwords)

# Lemmatization
nltk.download('wordnet')
def lemmatize(column):
    lemmatizer = WordNetLemmatizer()
    column = column.apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
    return column

df_fomc['clean text'] = lemmatize(df_fomc['clean text'])
df_reddit['clean text'] = lemmatize(df_reddit['clean text'])



# PART II: Sentiment Analysis
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def sentiment_analysis(df):
    '''
    Analyze the sentiment according to the text of each statement
    Return: dataframe with sentiment columns
    '''
    # Create lists to store sentiment scores
    compound_scores = []
    pos_scores = []
    neu_scores = []
    neg_scores = []

    # Iterate over rows in the DataFrame
    for i in range(len(df)):
        if df.equals(df_fomc):
            text = df.iloc[i]['Linked Content']
        else: 
            text = df.iloc[i]['text']

        # Run the polarity score on each text
        sentiment_scores = sia.polarity_scores(text)

        # Append the scores to the lists
        compound_scores.append(sentiment_scores['compound'])
        pos_scores.append(sentiment_scores['pos'])
        neu_scores.append(sentiment_scores['neu'])
        neg_scores.append(sentiment_scores['neg'])

    # Add sentiment columns to the DataFrame
    df['compound'] = compound_scores
    df['positive'] = pos_scores
    df['neutral'] = neu_scores
    df['negative'] = neg_scores

    return df

df_fomc_sentiment = sentiment_analysis(df_fomc)
df_reddit_sentiment = sentiment_analysis(df_reddit)


def sentiment_define(x):
    '''
    Define the compound grades into three sentiments,
    positive, neutral, and negative.
    '''
    # positive range: 0.3333 ~ 1
    # neutral range: -0.3333 ~ 0.3333
    # negative range: -1 ~ -0.3333
    up_b = 1
    lw_b = -1
    devided = 3
    threshold = (up_b - lw_b)/devided
    if x >= (up_b - threshold):
        return 'positive'
    elif x <= (lw_b + threshold):
        return 'negative'
    else:
        return 'neutral'

df_fomc_sentiment['sentiment'] = df_fomc_sentiment['compound'].apply(sentiment_define)
df_reddit_sentiment['sentiment'] = df_reddit_sentiment['compound'].apply(sentiment_define)

# Save Files
# df_fomc_sentiment.to_excel("FOMC sentiment analysis scores.xlsx", index=False)
# df_reddit_sentiment.to_excel("Reddit sentiment analysis scores.xlsx", index=False)



# PART III: Some Data Viz
# 1. Word Clouds (General)
def generate_word_cloud(data, text_column='', title=''):
    """
    Generate and display a word cloud for the specified text column in the DataFrame.
    """
    text_combined = ' '.join(data[text_column])
    word_cloud = WordCloud(width=1000, height=600, random_state=21, max_font_size=150, background_color='white').generate(text_combined)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(word_cloud, interpolation='bilinear')
    ax.set_title(title)
    ax.axis("off")
    return fig, ax

fig_fomc, ax_fomc = generate_word_cloud(df_fomc, text_column='clean text', title='FOMC Statement Word Cloud')
# Save images
# fig_fomc.savefig('wordcloud_fomc.png')

fig_reddit, ax_reddit = generate_word_cloud(df_reddit, text_column='clean text', title='Reddit Word Cloud')
# Save images
# fig_reddit.savefig('wordcloud_reddit.png')


# 2. Aggregate Sentiment Scores:
mean_compound = df_fomc_sentiment['compound'].mean()
mean_compound_rd = df_reddit_sentiment['compound'].mean()

data = {
    'Data Source': ['FOMC Statement', 'Reddit'],
    'Mean Compound Score': [mean_compound, mean_compound_rd]
}

df_mean_compound = pd.DataFrame(data)
# Save Files
# df_mean_compound.to_excel("Mean Compound Scores.xlsx", index=False)

# 3. Histogram of compound scores
def plot_sentiment_histogram(df, df_name):
    '''
    Generate a histogram of compound sentiment scores for a DataFrame.
    '''
    plt.figure(figsize=(10, 6))
    plt.hist(df['compound'], bins=20, color="#0c2d55", alpha=0.7)
    plt.title(f'Distribution of Compound Sentiment Scores for {df_name}')
    plt.xlabel('Compound Score')
    plt.ylabel('Frequency')

plot_sentiment_histogram(df_fomc_sentiment, 'FOMC Statement')
plot_sentiment_histogram(df_reddit_sentiment, 'Reddit')


# 4. Time Series Analysis:    
# FOMC Statement
plt.figure(figsize=(10, 6)) 
plt.plot(df_fomc_sentiment['Date'], df_fomc_sentiment['compound'])
plt.title('Time Series of Compound Sentiment Scores for FOMC Statement')
plt.xlabel('Date')
plt.ylabel('Compound Score')
# Save images 
# plt.savefig('fomc_sentiment_time_series.png')

# Reddit
df_reddit_sentiment['created_at'] = pd.to_datetime(df_reddit_sentiment['created_at'])
df_reddit_sentiment.set_index('created_at', inplace=True)
monthly_mean = df_reddit_sentiment['compound'].resample('M').mean() #plot it by month
plt.figure(figsize=(10, 6)) 
monthly_mean.plot(title='Mean Compound Score by Month for Reddit')
plt.xlabel('Date')
plt.ylabel('Mean Compound Score')
# Save images
# plt.savefig('reddit_sentiment_time_series.png')


# 5. Plot TOP20 unigrams and bigrams by frequency
def plot_top_n_bigrams(data, df_name, n=20, figsize=(10, 6)):
    """
    Plot the top N bigrams by frequency for a given DataFrame.
    """
    # Create a CountVectorizer with bigram tokenization
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    ngrams = vectorizer.fit_transform(data)
    
    # Calculate count values and vocabulary
    count_values = ngrams.toarray().sum(axis=0)
    vocab = vectorizer.vocabulary_
    
    # Create a DataFrame with frequency and words columns
    df_ngram = pd.DataFrame(sorted([(count_values[i], k) for k, i in vocab.items()], reverse=True),
                            columns=['frequency', 'words'])

    plt.figure(figsize=figsize)
    plt.bar(df_ngram['words'].head(n), df_ngram['frequency'].head(n), color='#0c2d55')
    plt.title(f'Top {n} Bigrams by Frequency for {df_name}')
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')

plot_top_n_bigrams(df_fomc_sentiment['clean text'], df_name='FOMC Statement')
plot_top_n_bigrams(df_reddit_sentiment['clean text'], df_name='Reddit')



# PART IV: Build a Simple Machine Learning Model
# Reddit :Using a classifier for sentiment analysis 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC

# Split the Data
X_train, X_test, y_train, y_test = train_test_split(df_reddit_sentiment['clean text'], df_reddit_sentiment['sentiment'], test_size=0.3, random_state=0)

# Feature Extraction
tfidf_vectorizer = TfidfVectorizer(min_df=5, max_df=0.8)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Using Support Vector Machines (SVM):
svm_model = SVC(kernel='rbf', C=1.0)
svm_model.fit(X_train_tfidf, y_train)
svm_pred = svm_model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, svm_pred)
print(f'Accuracy: {accuracy}')
print(classification_report(y_test, svm_pred))

# Cross-Validation (Testing Validation)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(svm_model, X_train_tfidf, y_train, cv=5)
print(f'Cross-Validation Scores: {scores}')


# References:
# Sentiment Analysis using SVM: https://medium.com/scrapehero/sentiment-analysis-using-svm-338d418e3ff1
# CountVectorizer: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer
# TfidfVectorizer: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
# Sentiment Analysis:https://realpython.com/python-nltk-sentiment-analysis/
# Lemmatization Approaches: https://www.geeksforgeeks.org/python-lemmatization-approaches-with-examples/
# NLP: https://www.geeksforgeeks.org/natural-language-processing-nlp-tutorial/
