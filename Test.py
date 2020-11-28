#https://benjaminbenben.com/lastfm-to-csv/
#https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import animation
from IPython.display import HTML
import numpy as np

### Creating new csv file with Year, Month, Day, Time columns
"""
history = pd.read_csv('LastFmHistory.csv', parse_dates=['Date'], dayfirst=False)
history.Date=pd.DatetimeIndex(history.Date).tz_localize('UTC').tz_convert('US/Eastern')
history['Year']= history['Date'].dt.year
history['Month']= history['Date'].dt.month
history['Day']= history['Date'].dt.day
history['Hour']= history['Date'].dt.hour
history['Weekday'] = history['Date'].dt.day_name()
history.to_csv('csv/LastFmHistoryCleaned.csv')"""



history = pd.read_csv('csv/LastFmHistoryCleaned.csv')
weather = pd.read_csv('csv/Weather.csv')
spotifyDataArchive = pd.read_csv('csv/data_w_genres.csv')
history = pd.merge(history, weather, on=['Month', 'Day'])




### Seperating Dataframe by year
history2020 = history[history.Year == 2020.0]
history2019 = history[history.Year == 2019.0]
history2018 = history[history.Year == 2018.0]
history2017 = history[history.Year == 2017.0]

### Working with 2020

## First getting data on each individual song I listen to
listened_to_tracks_2020 = pd.DataFrame(history, columns=['Track', 'Artist', 'Album']).drop_duplicates(subset=['Track'])

### Creating Dataframe for artist information
spotify_artist_data = pd.merge(listened_to_tracks_2020, spotifyDataArchive, on='Artist', how='inner')
spotify_artist_data = spotify_artist_data.drop_duplicates(subset='Artist', keep="last")
del spotify_artist_data['Album']
del spotify_artist_data['Track']


# Getting number of plays for each song
listened_to_tracks_2020['Plays'] = history2020['Track'].map(history2020['Track'].value_counts())

# Getting the most common Year a song is listened to
playback_hours = history2020.groupby('Track').Year.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_hours, on="Track")

# Getting the most common Month
playback_month = history2020.groupby('Track').Month.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_month, on="Track")

# Getting the most common time of day a song is listened to
playback_hours = history2020.groupby('Track').Hour.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_hours, on="Track")

# Getting average temperature for each Track
playback_temperature = history2020.groupby('Track').Temperature.median().to_frame()
listened_to_tracks_2020 = pd.merge(listened_to_tracks_2020, playback_temperature, on="Track")
listened_to_tracks_2020 = listened_to_tracks_2020.sort_values(['Plays'], ascending=[False]).reset_index()

listened_to_tracks_2020.to_csv('csv/listened_to_tracks_2020.csv')




### Creating Plots
fig = plt.figure(1)
fig.set_figheight(5)
fig.set_figwidth(13)
plt.rc('axes',edgecolor='#fafbfc')
plt.rcParams.update({'font.size': 8})
ax = fig.add_subplot(1, 1, 1)
rect = fig.patch
rect.set_facecolor('#24292e')


"""##Season vs Top Ten Artist
season_vs_topartists = pd.DataFrame(listened_to_tracks_2020, columns=['Artist', 'Month']).drop_duplicates(subset=['Artist']).head(10).reset_index()
del season_vs_topartists['index']
artists = season_vs_topartists['Artist']
seasons = season_vs_topartists['Month']
plt.bar(artists, seasons, color='#2dba4e')
ax = plt.gca()
ax.XColor ='#fafbfc'
ax.set_facecolor('#2b3137')
ax.tick_params(axis='x', colors='#fafbfc')
ax.set_xticks(range(len(artists)))
ax.set_xticklabels(artists, color='#fafbfc')
ax.set_yticks(range(12))
ax.set_yticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], color='#fafbfc')"""





##Temperature vs Top Ten Artist
temperature_vs_topartists = pd.DataFrame(listened_to_tracks_2020, columns=['Artist', 'Temperature']).drop_duplicates(subset=['Artist']).head(15).reset_index()
temperature_vs_topartists = temperature_vs_topartists.sort_values(['Temperature'], ascending=[True]).reset_index()
artists = temperature_vs_topartists['Artist']
temperatures = temperature_vs_topartists['Temperature']

plt.barh(artists, temperatures, color='#2dba4e')
for i, (plays, artist) in enumerate(zip(temperature_vs_topartists['Temperature'], temperature_vs_topartists['Artist'])):
       ax.text(plays, i, " " + str(plays), ha='left', color='#fafbfc')  # 38: plays
ax = plt.gca()
ax.XColor ='#fafbfc'
ax.set_facecolor('#2b3137')
ax.set_title('Top Artists vs. Temperature Outside', color='#fafbfc', fontsize=15, fontweight='bold')
ax.tick_params(axis='x', colors='#fafbfc')
ax.set_xlabel('Temperature Outside (°)', color='#fafbfc')
ax.set_yticks(range(len(artists)))
ax.set_yticklabels(artists, color='#fafbfc')
ax.set_xticks(np.arange(0, 100, step=10))
ax.set_xticklabels(np.arange(0, 100, step=10), color='#fafbfc')
plt.savefig('graphs/temperature_vs_topartists.png')
plt.close('all')




##Genre vs Month
artist_vs_month = pd.DataFrame(history2020, columns=['Artist', 'Month', 'Year'])
artist_vs_month = pd.merge(artist_vs_month, spotify_artist_data, how='inner', on='Artist')
artist_vs_month = pd.DataFrame(artist_vs_month, columns=['Artist', 'Month', 'Year'])
artist_vs_month = artist_vs_month.groupby(["Artist", "Month"]).size().reset_index(name="Plays")
artist_vs_month = artist_vs_month.drop_duplicates(subset=['Artist', 'Month']).sort_values('Month', ascending=False)
print(artist_vs_month)



fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(month):
       months = {1: 'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
       currentMonth = (artist_vs_month[artist_vs_month['Month'].eq(month)]
                       .sort_values(by='Plays', ascending=False)
                       .head(10))
       ax.clear()
       currentMonth = currentMonth[::-1]
       ax.barh(currentMonth['Artist'], currentMonth['Plays'], color='#2dba4e')
       dx = currentMonth['Plays'].max()
          # flip values from top to bottom
       # iterate over the values to plot labels and values
       for i, (plays, artist) in enumerate(zip(currentMonth['Plays'], currentMonth['Artist'])):
              ax.text(plays, i, artist + " ", ha='right', size=15)  # khalid: name
              ax.text(plays, i, " " + str(plays), ha='left',size=15)  # 38: plays


       ax.text(1, 0.4, months[month], transform=ax.transAxes, color='#2b3137', size=46, ha='right', weight=800)
       ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
       ax.xaxis.set_ticks_position('top')
       ax.tick_params(axis='x', colors='#777777', labelsize=12)
       ax.set_yticks([])
       ax.margins(0, 0.01)
       ax.grid(which='major', axis='x', linestyle='-')
       ax.set_axisbelow(True)
       ax.text(0, 1.1, 'Monthly Top Artists',
               transform=ax.transAxes, size=24, weight=600, ha='left')
       ax.text(0, 1.06, 'Plays', transform=ax.transAxes, size=12, color='#777777')
       plt.box(False)


fig, ax = plt.subplots(figsize=(17, 9))
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1, 11))
Writer = animation.writers['pillow']
writer = Writer(fps=.55, metadata=dict(artist='Me'), bitrate=1000)
HTML(animator.save('animation.gif', writer=writer))







