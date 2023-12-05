# -*- coding: utf-8 -*-
"""
Scrape S&P 500 from March 2022 to March 2023

"""
import os
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Import Dataframes
path = r"C:\Users\user\Documents\GitHub\final-project-redditpower"
df_fomc = pd.read_excel(os.path.join(path, 'FOMC sentiment analysis scores.xlsx'))
df_reddit = pd.read_excel(os.path.join(path, 'Reddit sentiment analysis scores.xlsx'))


# Scraping Stock prices
df_sp500= yf.download('%5EGSPC', start='2022-03-01', end='2023-03-31')
df_dow = yf.download('%5EDJI?p=%5EDJI', start='2022-03-01', end='2023-03-31')


# Adjust Date Columns (Set the timezone to 'UTC' for datetime columns)
df_sp500.reset_index(inplace=True)
df_dow.reset_index(inplace=True)
df_sp500['Date'] = pd.to_datetime(df_sp500['Date']).dt.tz_localize('UTC')
df_dow['Date'] = pd.to_datetime(df_dow['Date']).dt.tz_localize('UTC')

df_fomc['Date'] = pd.to_datetime(df_fomc['Date']).dt.tz_localize('UTC')
df_reddit['created_at'] = pd.to_datetime(df_reddit['created_at']).dt.tz_localize('UTC')

# Data Viz
# Create a dual-axis chart for S&P 500 and FOMC Compound
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(df_fomc['Date'], df_fomc['compound'], color='green', marker='o')
ax2.plot(df_sp500['Date'], df_sp500['Close'], color='blue')
ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax1.set_xlabel('Date')
ax1.set_ylabel('FOMC Compound')
ax2.set_ylabel('S&P 500 Close')
plt.title('Comparison of S&P 500 Close and FOMC Compound')
plt.show()

# Create a dual-axis chart for Dow Jones and FOMC Compound
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(df_fomc['Date'], df_fomc['compound'], color='green', marker='o')
ax2.plot(df_dow['Date'], df_dow['Close'], color='blue')
ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax1.set_xlabel('Date')
ax1.set_ylabel('FOMC Compound')
ax2.set_ylabel('Dow Jones Close')
plt.title('Comparison of Dow Jones Close and FOMC Compound')
plt.show()

# Create a dual-axis chart for S&P 500 and Reddit Compound
monthly_mean = df_reddit.resample('D', on='created_at').mean()
monthly_mean.reset_index(inplace=True)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(monthly_mean['created_at'], monthly_mean['compound'], color='green', marker='o')
ax2.plot(df_sp500['Date'], df_sp500['Close'], color='blue')
ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax1.set_xlabel('Date')
ax1.set_ylabel('Reddit Compound')
ax2.set_ylabel('S&P 500 Close')
plt.title('Comparison of S&P 500 Close and Reddit Compound')
plt.show()





model = sm.OLS(df_sp500['Close'], df_reddit['compound'])


# References:
# Scrape Yahoo Finance: https://weikaiwei.com/finance/yfinance/