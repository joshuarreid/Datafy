#https://benjaminbenben.com/lastfm-to-csv/
import pandas as pd


### Creating new csv file with Year, Month, Day, Time columns
"""
history = pd.read_csv('LastFmHistory.csv', parse_dates=['Date'], dayfirst=False)
history['Year']= history['Date'].dt.year
history['Month']= history['Date'].dt.month
history['Day']= history['Date'].dt.day
history['Hour']= history['Date'].dt.hour
history.to_csv('History.csv')
print(history.head())"""


history = pd.read_csv('History.csv')

### Seperating Dataframe by year
history2020 = history[history.Year == 2020.0]
history2019 = history[history.Year == 2019.0]
history2018 = history[history.Year == 2018.0]
history2017 = history[history.Year == 2017.0]

### Working with 2020

## First getting data on each individual song I listen to
listened_to_tracks = history2020['Track'].unique()



















"""
from matplotlib import pyplot as plt

days = [0,1,2,3,4,5,7]
money_spent = [10, 12, 12,10,14,22,1]

plt.plot(days, money_spent)
plt.show()"""