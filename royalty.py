import csv
import sys
import pandas as pd
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import discogs_client
from itertools import combinations

d = discogs_client.Client('ReleaseDateProject', user_token='AauEetKJPOXvRmEgaxzrvqdGTexBTPkHJSsvGaew')

arg = " ".join(sys.argv[1:])
songs = {}
releaseDates = {}
writerData = {}
file = open(arg)
fileCSV = csv.reader(file)
df = pd.read_csv(arg)
filtered_df = pd.read_csv(arg, usecols=['WORK_TITLE', 'WRITERS'])

for rows in range(len(filtered_df)):
    temp = filtered_df.loc[rows, "WORK_TITLE"]
    if temp not in writerData:
        tempRow = filtered_df.loc[rows, "WRITERS"]
        tempNames = str(tempRow)
        allWriters = []
        tempFirst = ''
        nameDone = False
        tempLast = ''
        metComma = False
        fullDone = False
        newName = False
        for i in range(len(tempNames)):
            if tempNames[i].isalpha() and metComma is False:
                tempLast += tempNames[i]
            elif tempNames[i].isalpha() and metComma is True and fullDone is False:
                tempFirst += tempNames[i]
            elif tempNames[i] == ',':
                metComma = True
            elif tempNames[i] == ' ' and nameDone is False and newName is False:
                nameDone = True
            elif tempNames[i - 1] == ';':
                newName = False
            elif tempNames[i] == ' ' and nameDone is True and fullDone is False:
                tempFinal = tempFirst + ' ' + tempLast
                allWriters.append(tempFinal)
                fullDone = True
            elif tempNames[i] == ';':
                tempFirst = ''
                tempLast = ''
                metComma = False
                nameDone = False
                fullDone = False
                newName = True

        comboAllWriters = list()

        for n in range(len(allWriters)):
            comboAllWriters += list(combinations(allWriters, n))

        comboAllWriters.reverse()
        print(comboAllWriters)
        writerData.update({temp: comboAllWriters})

for rows in range(len(filtered_df)):
    temp = filtered_df.loc[rows, "WORK_TITLE"]
    if temp not in songs:
        time.sleep(1.2)
        print(temp)
        print(len(writerData.get(temp)))
        for i in range(len(writerData.get(temp))):
            writersStr = ', '
            writersStr = writersStr.join(writerData.get(temp)[i])
            print(writersStr)
            time.sleep(1)
            result = d.search(track=temp, credit=writersStr, type='release')
            if result:
                tempArtist = str(result[0].artists[0])
                searchResult = re.search("'(.*)'", tempArtist)
                if searchResult.group():
                    artist = (searchResult.group(1))
                    artist = re.sub(r'[^a-zA-Z ]', '',artist)
                    if artist != 'Various':
                        songs.update({temp: artist})
                        print('FINAL ARTIST:   ' + artist)
                        break
                else:
                    songs.update({temp: 'NO RELEASE DATE FOUND'})


            else:
                songs.update({temp: 'NO RELEASE DATE FOUND'})


print(songs)

for key in songs:
    print(key + '=============================================================')
    releaseDates.update({key: '9999-99-99'})
    currYear = 9999
    currMonth = 99
    currDay = 99
    if songs.get(key) != 'NO RELEASE DATE FOUND':
        search_str = key + ' ' + songs.get(key)
        print("SEARCH: " + search_str + '||||||||||||||||||||||||||||||||||||||')
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('c1611288f223493199191f4f47f8f2b5', '810645cfbff04f6a9409083e56d15b2a'))
        result = sp.search(search_str)

        for track in result['tracks']['items'][:10]:
            if track['album']['release_date']:
                print(key + '   ' + track['album']['release_date'])
                tempDate = track['album']['release_date']
                if len(tempDate) > 7:
                    tempYear = int(tempDate[0:4])
                    tempMonth = int(tempDate[5:7])
                    tempDay = int(tempDate[8])
                    currDate = releaseDates.get(key)
                    currYear = int(currDate[0:4])
                    currMonth = int(currDate[5:7])
                    currDay = int(currDate[8])
                elif 4 < len(tempDate) < 8:
                    tempYear = int(tempDate[0:4])
                    tempMonth = int(tempDate[5:7])
                    tempDay = int(99)
                    currDate = releaseDates.get(key)
                    currYear = int(currDate[0:4])
                    currMonth = int(currDate[5:7])
                    currDay = int(currDate[8])
                elif len(tempDate) < 5:
                    tempYear = int(tempDate[0:4])
                    tempMonth = int(99)
                    tempDay = int(99)
                    currDate = releaseDates.get(key)
                    currYear = int(currDate[0:4])
                    currMonth = int(currDate[5:7])
                    currDay = int(currDate[8])

                if tempYear <= currYear and tempMonth <= currMonth and tempDay <= currDay:
                    releaseDates.update({key: tempDate})
                    print("CHANGED " + tempDate + "   " + key)

releaseList = []
for rows in range(len(df)):
    temp = filtered_df.loc[rows, "WORK_TITLE"]
    releaseList.append(releaseDates.get(temp))

with open('FullSongDatabase.csv', 'w') as f:
    writer = csv.writer(f)
    for k, v in releaseDates.items():
        writer.writerow([k, v])

arg = arg.replace('/', '-')
print(arg)
df2 = df.copy()
#df2["Release Dates"] = releaseList
print(df2)
df2.to_csv('FinalSheets/WITH-RELEASE-DATES-' + arg, index=False)
