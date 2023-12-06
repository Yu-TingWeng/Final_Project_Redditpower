"""
Comparison between Stock Price and FOMC Statement, Reddit
"""
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

df_fomc = pd.read_excel('FOMC sentiment analysis scores.xlsx')
df_reddit = pd.read_excel('Reddit sentiment analysis scores.xlsx')

# Scraping stock prices from Yahoo! finance
def scrape_stock(ticker, start_date, end_date):
    df_stock = yf.download(ticker, 
                           start=start_date, 
                           end=end_date
                           )
    df_stock.reset_index(inplace=True)
    return df_stock

df_sp500 = scrape_stock('%5EGSPC', 
                        '2022-03-01', 
                        '2023-03-31'
                        )
df_dow = scrape_stock('%5EDJI?p=%5EDJI', 
                      '2022-03-01', 
                      '2023-03-31'
                      )
df_nasdaq = scrape_stock('^IXIC', 
                         '2022-03-01', 
                         '2023-03-31'
                         )

# Renaming the 'created_at' column in Reddit dataframe to 'Date' to aid dt
# object processing
df_reddit.rename(columns={'created_at': 'Date'}, inplace=True)

# Unify datetime formats
def timezone_adjust(df, timezone):
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(timezone)
    return df

timezone = 'UTC'
df_fomc = timezone_adjust(df_fomc, 
                          timezone
                          )
df_reddit = timezone_adjust(df_reddit, 
                            timezone
                            )
df_sp500 = timezone_adjust(df_sp500, 
                           timezone
                           )
df_dow = timezone_adjust(df_dow, 
                         timezone
                         )
df_nasdaq = timezone_adjust(df_nasdaq, 
                            timezone
                            )

def stock_plotter(df1, df2, y1_label, y2_label, title, color1, color2):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(df1['Date'], 
             df1['compound'], 
             color=color1, 
             marker='o'
             )
    ax2.plot(df2['Date'], 
             df2['Close'], 
             color=color2
             )
    ax2.tick_params(axis='x', 
                    which='both', 
                    bottom=False, 
                    top=False, 
                    labelbottom=False
                    )
    ax1.set_xlabel('Date')
    ax1.set_ylabel(y1_label)
    ax2.set_ylabel(y2_label)
    plt.title(title)
    plt.show()

monthly_mean = df_reddit.resample('10D', on='Date').mean()
monthly_mean.reset_index(inplace=True)

stock_plotter(df_fomc, 
              df_sp500, 
              'FOMC Compound', 
              'S&P 500 Close', 
              'Comparison of S&P 500 Close and FOMC Compound', 
              'darkgreen', 
              'blue'
              )
stock_plotter(df_fomc, 
              df_dow, 
              'FOMC Compound', 
              'S&P 500 Close', 
              'Comparison of Dow Jones Close and FOMC Compound', 
              'darkgreen', 
              'maroon'
              )
stock_plotter(df_fomc, 
              df_nasdaq, 
              'FOMC Compound', 
              'S&P 500 Close', 
              'Comparison of NASDAQ Close and FOMC Compound', 
              'darkgreen', 
              'black'
              )
stock_plotter(monthly_mean, 
              df_sp500, 
              'Reddit Compound', 
              'S&P 500 Close', 
              'Comparison of S&P 500 Close and Reddit Compound', 
              '#FF5700', 
              'blue'
              )
stock_plotter(monthly_mean, 
              df_dow, 
              'Reddit Compound', 
              'Dow Jones Close', 
              'Comparison of Dow Jones Close and Reddit Compound', 
              '#FF5700', 
              'maroon'
              )
stock_plotter(monthly_mean, 
              df_nasdaq, 
              'Reddit Compound', 
              'NASDAQ Close', 
              'Comparison of NASDAQ Close and Reddit Compound', 
              '#FF5700', 
              'black'
              )

#####
# OLS
def ols_analysis(df, stock_df, y_column='Close', x_column='compound'):
    # Merge DataFrames on 'Date'
    merged_df = pd.merge(df, stock_df, on='Date', how='inner')
    # Set up the OLS model
    X = sm.add_constant(merged_df[x_column])
    model = sm.OLS(merged_df[y_column], X).fit()
    # Print the model summary
    print(model.summary())
    
    # Calculate the correlation coefficient
    correlation = np.corrcoef(merged_df[x_column], merged_df[y_column])

    return model, correlation

# FOMC & NASDAQ
fomc_nasdaq = pd.merge(df_fomc, df_nasdaq, on='Date', how='inner')
model_fomc_nasdaq, cor_fomc_nasdaq= ols_analysis(df_fomc, df_nasdaq)

# FOMC & Dow Jones
fomc_dow = pd.merge(df_fomc, df_dow, on='Date', how='inner')
model_fomc_dow, cor_fomc_dow = ols_analysis(df_fomc, df_dow)

# FOMC & S&P500
fomc_sp500 = pd.merge(df_fomc, df_sp500, on='Date', how='inner')
model_fomc_sp500, cor_fomc_sp500 = ols_analysis(df_fomc, df_sp500)

# Reddit & NASDAQ
reddit_nasdaq = pd.merge(monthly_mean, df_nasdaq, on='Date', how='inner')
model_reddit_nasdaq, cor_reddit_nasdaq= ols_analysis(monthly_mean, df_nasdaq)

# Reddit & Dow Jones
reddit_dow = pd.merge(monthly_mean, df_dow, on='Date', how='inner')
model_reddit_dow, cor_reddit_dow = ols_analysis(monthly_mean, df_dow)

# Reddit & S&P500
reddit_sp500 = pd.merge(monthly_mean, df_sp500, on='Date', how='inner')
model_reddit_sp500, cor_reddit_sp500 = ols_analysis(monthly_mean, df_sp500)
