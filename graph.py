# imports
from matplotlib import pyplot as plt
import omdb
import xml.etree.ElementTree as ET
import numpy as np

# Default values
MY_KEY = 'xxxxxxxx'
TITLE  = 'Breaking bad' 
DATA = []

# read key (stored seperately)
# get your own at http://www.omdbapi.com/apikey.aspx
infile = open("key.txt", "r")
MY_KEY = infile.readline().rstrip()
infile.close()

if MY_KEY == 'xxxxxxxx':
    print("Key unsuccesfully read")
    exit()

# get user input
# TODO

# setup omdb
# structure of overall data:
# < root with attribute response >
#   <movie with attributes title, year, rated, released, runtime, genre, director, writer, 
#                          actors, plot, language, country, awards, poster (rul), metascore,
#                          imdbRating, imdbVotes, imdbID, type />
# < /root >
omdb.set_default('tomatoes',True)
client = omdb.OMDBClient(apikey=MY_KEY)
overall = client.request(t=TITLE,r='xml')
xml_overall = overall.content
root = ET.fromstring(xml_overall)

# TODO: movie functionality
if root[0].attrib['type'] != 'series':
    print("This program only supports series")
    exit


# obtain data
# structure of seasonal data: 
# < root with attributes Title, Season, totalSeasons, Response >
#   <result with attributes Title, Released, Episode, imdbRating, imdbID />
#    ...
#   <result with attributes Title, Released, Episode, imdbRating, imdbID />
# < /root >
current_season = 0
while True:
    current_season += 1
    season_info = client.request(t=TITLE,r='xml',season=current_season)
    xml_season_info = ET.fromstring(season_info.content)

    # extract useful data to array
    # TODO: currently only ratings
    try:
        DATA.append([float(episode.attrib['imdbRating']) for episode in xml_season_info])
    except:
        print('Your series has an invalid format: episode rating missing (season {})'.format(current_season))
    
    if current_season == int(xml_season_info.attrib['totalSeasons']):
        break

# plot data
last_ep_plotted = 0
for snr in range(0,len(DATA)):
    season_data = DATA[snr]
    data_x = [last_ep_plotted + i for i in range(1,1+len(season_data))]
    plt.scatter(data_x, season_data, label='season {} ({})'.format(snr + 1, np.round(np.average(season_data),2)))
    last_ep_plotted += len(season_data)

    # plot seasons trendline
    z = np.polyfit(data_x, season_data, 1)
    p = np.poly1d(z)
    plt.plot(data_x,p(data_x),"-")

#plot series trendline
flat_data  = [item for sublist in DATA for item in sublist]
flat_xaxis = [i for i in range(1,len(flat_data) + 1)]
z = np.polyfit(flat_xaxis, flat_data, 1)
p = np.poly1d(z)
plt.plot(flat_xaxis,p(flat_xaxis),"r--")

# plot make-up
plt.legend()
plt.xlabel('Episodes')
plt.ylabel('Ratings')
plt.title('Episode ratings for {}'.format(TITLE))

plt.show()
