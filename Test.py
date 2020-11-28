#https://benjaminbenben.com/lastfm-to-csv/
import pandas as pd
import numpy as np
import Statify.Statify as lastFm


### Creating new csv file with Year, Month, Day, Time columns
"""
history = pd.read_csv('LastFmHistory.csv', parse_dates=['Date'], dayfirst=False)
history.Date=pd.DatetimeIndex(history.Date).tz_localize('UTC').tz_convert('US/Eastern')
history['Year']= history['Date'].dt.year
history['Month']= history['Date'].dt.month
history['Day']= history['Date'].dt.day
history['Hour']= history['Date'].dt.hour
history['Weekday'] = history['Date'].dt.day_name()
history.to_csv('History.csv')"""



history = pd.read_csv('History.csv')
weather = pd.read_csv('Weather.csv')
history = pd.merge(history, weather, on=['Month', 'Day'])




### Seperating Dataframe by year
history2020 = history[history.Year == 2020.0]
history2019 = history[history.Year == 2019.0]
history2018 = history[history.Year == 2018.0]
history2017 = history[history.Year == 2017.0]

### Working with 2020

## First getting data on each individual song I listen to
listened_to_tracks_2020 = pd.DataFrame(history, columns=['Track', 'Artist', 'Album']).drop_duplicates(subset=['Track'])

# Getting number of plays for each song
listened_to_tracks_2020['Plays'] = history['Track'].map(history['Track'].value_counts())

# Getting the most common Year a song is listened to
playback_hours = history.groupby('Track').Year.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_hours, on="Track")

# Getting the most common Month
playback_month = history.groupby('Track').Month.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_month, on="Track")

# Getting the most common time of day a song is listened to
playback_hours = history.groupby('Track').Hour.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_hours, on="Track")

# Getting average temperature for each Track
playback_temperature = history.groupby('Track').Temperature.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_temperature, on="Track")
listened_to_tracks_2020 = listened_to_tracks_2020.sort_values(['Plays', 'Temperature'], ascending=[False, False]).reset_index()

listened_to_tracks_2020.to_csv('ListeningData.csv')









"""
from matplotlib import pyplot as plt

days = [0,1,2,3,4,5,7]
money_spent = [10, 12, 12,10,14,22,1]

plt.plot(days, money_spent)
plt.show()"""