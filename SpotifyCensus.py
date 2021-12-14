#SpotifyCensus project
#Team members: Anders Lundin, Nathan Witt, Ryan Horlick

import requests
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

CLIENT_ID = '3d63895403d14aa7833edba57df85660'
CLIENT_SECRET = '1dd33174539444ec9046878a0368ec87'
AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)

sp = spotipy.Spotify(auth_manager=auth_manager)

#takes the id from each dictionary and makes a list of ids
def getsongs(pl):
    newli = []
    for song in pl:
        newli.append(song["song"])
    return newli

#takes dictionary of artists and song names and searches spotify for them, returning a list of dictionaries for each song with id, track, artist, and genres. 
def get_info(d, limit=25, offset=0):
    queries =[]
    for key in d:
        queries.append(d[key]["song_name"] + " " + d[key]["artist"])
    listinfo = []
    for q in queries[offset:offset+25]:
        songdict = {}
        qres = sp.search(q)
        track = qres["tracks"]["items"][0]
        songdict["id"] = track["id"]
        songdict["track"] = track["name"]
        artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
        songdict["artist"] = artist["name"]
        songdict["genres"] = artist["genres"]
        listinfo.append(songdict)

    return listinfo

#take a list of dictionaries with info, returns audio features of each track in a list
def get_audio_info(li):
    new = []
    for d in li:
        new.append(sp.audio_features(d["id"]))
    return(new)


# scrapes 
def scrape_top_music(year):

    url = f"https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', {'class':'wikitable'}).find('tbody')
    songs = table.find_all('tr')
    songs.pop(0)


    song_dict = {}
    for song in songs:
        rank = str((song.find_all('td'))[0].text)
        song_dict[rank] = {}
        links = song.find_all('a')
        song_dict[rank]['song_name'] = links[0].text
        song_dict[rank]['artist'] = links[1].text

    return song_dict

def wiki_tables():
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS wiki2000 ('track' TEXT PRIMARY KEY, 'artist' TEXT)")
    wiki2000 = scrape_top_music(2000)
    for num in wiki2000:
        cur.execute('INSERT OR IGNORE INTO wiki2000 (track, artist) VALUES (?,?)', (wiki2000[num]['song_name'], wiki2000[num]['artist']))
    

    cur.execute("CREATE TABLE IF NOT EXISTS wiki2010 ('track' TEXT PRIMARY KEY, 'artist' TEXT)")
    wiki2010 = scrape_top_music(2010)
    for num in wiki2010:
        cur.execute('INSERT OR IGNORE INTO wiki2010 (track, artist) VALUES (?,?)', (wiki2010[num]['song_name'], wiki2010[num]['artist']))
    

    cur.execute("CREATE TABLE IF NOT EXISTS wiki2020 ('track' TEXT PRIMARY KEY, 'artist' TEXT)")
    wiki2020 = scrape_top_music(2020)
    for num in wiki2020:
        cur.execute('INSERT OR IGNORE INTO wiki2020 (track, artist) VALUES (?,?)', (wiki2020[num]['song_name'], wiki2020[num]['artist']))
    conn.commit()
    return(wiki2000, wiki2010, wiki2020)

def spotify_tables(count2000):
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()

    wiki2000 = wiki_tables()[0]
    wiki2010 = wiki_tables()[1]
    wiki2020 = wiki_tables()[2]
    top2000 = get_info(wiki2000, 25, int(count2000[0][0]))

    cur.execute("SELECT COUNT('id') FROM billboard2010")
    count2010 = cur.fetchall()
    top2010 = get_info(wiki2010, 25, int(count2010[0][0]))

    cur.execute("SELECT COUNT('id') FROM billboard2020")
    count2020 = cur.fetchall()
    top2020 = get_info(wiki2020, 25, int(count2020[0][0]))

    for d in top2000:
        gs = ""
        for genre in d["genres"]:
            gs += genre + ", "
        d["genres"] = gs
        cur.execute('INSERT INTO billboard2000 (id, track, artist, genres) VALUES (?,?,?,?)', (d['id'], d['track'], d['artist'], d['genres']))
    for d in top2010:
        gs = ""
        for genre in d["genres"]:
            gs += genre + ", "
        d["genres"] = gs
        cur.execute('INSERT INTO billboard2010 (id, track, artist, genres) VALUES (?,?,?,?)', (d['id'], d['track'], d['artist'], d['genres']))
    for d in top2020:
        gs = ""
        for genre in d["genres"]:
            gs += genre + ", "
        d["genres"] = gs
        cur.execute('INSERT INTO billboard2020 (id, track, artist, genres) VALUES (?,?,?,?)', (d['id'], d['track'], d['artist'], d['genres']))
    
    #making tables for audio info
    audio2000 = get_audio_info(top2000)
    audio2010 = get_audio_info(top2010)
    audio2020 = get_audio_info(top2020)

    cur.execute("CREATE TABLE IF NOT EXISTS audio2000 ('id' TEXT PRIMARY KEY, 'danceability' REAL, 'energy' REAL, 'liveness' REAL, 'tempo' REAL)")
    for d in audio2000:
        d = d[0]
        cur.execute('INSERT INTO audio2000 (id, danceability, energy, liveness, tempo) VALUES (?,?,?,?,?)', (d['id'], d['danceability'], d['energy'], d['liveness'], d['tempo']))

    cur.execute("CREATE TABLE IF NOT EXISTS audio2010 ('id' TEXT PRIMARY KEY, 'danceability' REAL, 'energy' REAL, 'liveness' REAL, 'tempo' REAL)")
    for d in audio2010:
        d = d[0]
        cur.execute('INSERT INTO audio2010 (id, danceability, energy, liveness, tempo) VALUES (?,?,?,?,?)', (d['id'], d['danceability'], d['energy'], d['liveness'], d['tempo']))

    cur.execute("CREATE TABLE IF NOT EXISTS audio2020 ('id' TEXT PRIMARY KEY, 'danceability' REAL, 'energy' REAL, 'liveness' REAL, 'tempo' REAL)")
    for d in audio2020:
        d = d[0]
        cur.execute('INSERT INTO audio2020 (id, danceability, energy, liveness, tempo) VALUES (?,?,?,?,?)', (d['id'], d['danceability'], d['energy'], d['liveness'], d['tempo']))

    conn.commit()

# Make a dictionary of how frequently each artist is on the top 100
def artist_frequency():
    f= open("documentation.txt","w")
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()

    cur.execute("SELECT artist FROM wiki2000")
    artists = cur.fetchall()
    ad1 = {}
    for artist in artists:
        for name in artist:
            if name not in ad1:
                ad1[name] = 0
            ad1[name] += 1
    ad1 = dict(sorted(ad1.items(), key=lambda item: item[1], reverse=True))

    cur.execute("SELECT artist FROM wiki2010")
    artists = cur.fetchall()
    ad2 = {}
    for artist in artists:
        for name in artist:
            if name not in ad2:
                ad2[name] = 0
            ad2[name] += 1
    ad2 = dict(sorted(ad2.items(), key=lambda item: item[1], reverse=True))

    cur.execute("SELECT artist FROM wiki2020")
    artists = cur.fetchall()
    ad3 = {}
    for artist in artists:
        for name in artist:
            if name not in ad3:
                ad3[name] = 0
            ad3[name] += 1
    ad3 = dict(sorted(ad3.items(), key=lambda item: item[1], reverse=True))
    conn.commit()
    f.write("Each artist dictionary shows the frequency of appearances on the billboard 100 for each respective year.\n")
    f.write("\nArtist dictionary for 2000:\n" + str(ad1.items()))
    f.write("\nArtist dictionary for 2010:\n" + str(ad2.items()))
    f.write("\nArtist dictionary for 2020:\n" + str(ad3.items()))
    f.close()
    return (ad1, ad2, ad3)

#first, get a dictionary of how frequently genres appear. Next, find the average danceability, energy, liveness, and tempo for each year
def year_analysis():
    f= open("documentation.txt", "a+")
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()
    sumli =[]
    ad1 = artist_frequency()[0]
    ad2 = artist_frequency()[1]
    ad3 = artist_frequency()[2]
    cur.execute("SELECT billboard2000.id, billboard2000.track, billboard2000.artist, billboard2000.genres, audio2000.danceability, audio2000.energy, audio2000.liveness, audio2000.tempo FROM audio2000 JOIN billboard2000 ON audio2000.id = billboard2000.id WHERE billboard2000.id = audio2000.id")
    rows = cur.fetchall()
    gd = {}
    dancesum = 0
    energysum = 0
    livesum = 0
    temposum = 0
    for row in rows:
        for string in row[3].split(", "):
            string = string.strip()
            if string not in gd:
                if string != "" and string != " ":
                    gd[string] = 0
            if string != "" and string != " ":
                gd[string] += 1
        dancesum += row[4]
        energysum += row[5]
        livesum += row[6]
        temposum += row[7]
    gd = dict(sorted(gd.items(), key=lambda item: item[1], reverse=True))
    danceave = dancesum / 100
    energyave = energysum / 100
    liveave = livesum / 100
    tempoave = temposum /100
    adav = {}
    for num in ad1.values():
        if num not in adav:
            adav[num] = 0
        adav[num] += 1
    sumli.append(("sum2000:", gd, danceave, energyave, liveave, tempoave, adav))

    cur.execute("SELECT billboard2010.id, billboard2010.track, billboard2010.artist, billboard2010.genres, audio2010.danceability, audio2010.energy, audio2010.liveness, audio2010.tempo FROM audio2010 JOIN billboard2010 ON audio2010.id = billboard2010.id WHERE billboard2010.id = audio2010.id")
    rows = cur.fetchall()
    gd = {}
    dancesum = 0
    energysum = 0
    livesum = 0
    temposum = 0
    for row in rows:
        for string in row[3].split(", "):
            string = string.strip()
            if string not in gd:
                if string != "" and string != " ":
                    gd[string] = 0
            if string != "" and string != " ":
                gd[string] += 1
        dancesum += row[4]
        energysum += row[5]
        livesum += row[6]
        temposum += row[7]
    gd = dict(sorted(gd.items(), key=lambda item: item[1], reverse=True))
    danceave = dancesum / 100
    energyave = energysum / 100
    liveave = livesum / 100
    tempoave = temposum /100
    adav = {}
    for num in ad2.values():
        if num not in adav:
            adav[num] = 0
        adav[num] += 1
    sumli.append(("sum2010:", gd, danceave, energyave, liveave, tempoave, adav))

    cur.execute("SELECT billboard2020.id, billboard2020.track, billboard2020.artist, billboard2020.genres, audio2020.danceability, audio2020.energy, audio2020.liveness, audio2020.tempo FROM audio2020 JOIN billboard2020 ON audio2020.id = billboard2020.id WHERE billboard2020.id = audio2020.id")
    rows = cur.fetchall()
    gd = {}
    dancesum = 0
    energysum = 0
    livesum = 0
    temposum = 0
    for row in rows:
        for string in row[3].split(", "):
            string = string.strip()
            if string not in gd:
                if string != "" and string != " ":
                    gd[string] = 0
            if string != "" and string != " ":
                gd[string] += 1
        dancesum += row[4]
        energysum += row[5]
        livesum += row[6]
        temposum += row[7]
    gd = dict(sorted(gd.items(), key=lambda item: item[1], reverse=True))
    danceave = dancesum / 100
    energyave = energysum / 100
    liveave = livesum / 100
    tempoave = temposum /100
    adav = {}
    for num in ad3.values():
        if num not in adav:
            adav[num] = 0
        adav[num] += 1
    sumli.append(("sum2020:", gd, danceave, energyave, liveave, tempoave, adav))
    conn.commit()
    f.write("\n\nEach summary list gives a dictionary of genres and their frequency in the top 100 that year, along with the average danceability, energy, liveness, and tempo of the songs on the chart. Finally, dictionaries of how many times an artist appeared on the billboard at x appearances is calculated (if key is 3, and value is 1, one artist appeared three times on the billboard).\n")
    f.write("\nSummary of data for 2000:\n")
    f.write("Genre frequencies: " + str(sumli[0][1]) + "\n")
    f.write("Average danceability: " + str(sumli[0][2]) + "\n")
    f.write("Average energy: " + str(sumli[0][3]) + "\n")
    f.write("Average liveness: " + str(sumli[0][4]) + "\n")
    f.write("Average tempo: " + str(sumli[0][5]) + "\n")
    f.write("Frequency of appearances for each artist: " + str(sumli[0][6]) + "\n\n")
    
    f.write("\nSummary of data for 2010:\n")
    f.write("Genre frequencies: " + str(sumli[1][1]) + "\n")
    f.write("Average danceability: " + str(sumli[1][2]) + "\n")
    f.write("Average energy: " + str(sumli[1][3]) + "\n")
    f.write("Average liveness: " + str(sumli[1][4]) + "\n")
    f.write("Average tempo: " + str(sumli[1][5]) + "\n")
    f.write("Frequency of appearances for each artist: " + str(sumli[1][6]) + "\n\n")

    f.write("\nSummary of data for 2020:\n")
    f.write("Genre frequencies: " + str(sumli[2][1]) + "\n")
    f.write("Average danceability: " + str(sumli[2][2]) + "\n")
    f.write("Average energy: " + str(sumli[2][3]) + "\n")
    f.write("Average liveness: " + str(sumli[2][4]) + "\n")
    f.write("Average tempo: " + str(sumli[2][5]) + "\n")
    f.write("Frequency of appearances for each artist: " + str(sumli[2][6]) + "\n\n")

    f.close()
    return(sumli)

# audio analyses line chart
def audio_lines(sumli):
    danceabilities = [sumli[0][2], sumli[1][2], sumli[2][2]]
    energies = [sumli[0][3], sumli[1][3], sumli[2][3]]
    livenesses = [sumli[0][4], sumli[1][4], sumli[2][4]]
    years = ["2000", "2010", "2020"]

    plt.title("Average audio analyses over time")
    plt.xlabel("Year")
    plt.ylabel("Amount from 0-1")


    x1 = np.array(years)
    y1 = np.array(danceabilities)
    x2 = np.array(years)
    y2 = np.array(energies)
    x3 = np.array(years)
    y3 = np.array(livenesses)

    plt.plot(x1, y1, "-b", label="danceability")
    plt.plot(x2, y2, "-r", label="energy")
    plt.plot(x3, y3, "-g", label="liveness")
    
    plt.legend(loc="upper right")
    plt.show()

#making the pie charts for genre distribution
def genre_pies(sumli):
    notshownsums = []
    shownlens = []
    genretotals = []
    disp =[]
    allsums =[]
    for tup in sumli:
        total = 0
        totalall = 0
        gens = list(tup[1].items())
        genretotals.append(len(gens))
        displayed = gens[:11]
        disp.append(displayed)
        summed = gens[11:]
        shownlen = len(gens)
        shownlens.append(shownlen)
        for tup in gens:
            totalall += tup[1]
        for tup in summed:
            total += tup[1]
        notshownsums.append(total)
        allsums.append(totalall)

    disp2000 = dict(disp[0])
    mylabels = list(disp2000.keys())
    total = 0
    for num in disp2000.values():
        total += num
    percent2000 = []
    for num in disp2000.values():
        percent2000.append(num/total)
    y = np.array(percent2000)
    plt.pie(y, labels = mylabels)
    plt.suptitle("% make up of top 10 genres in 2000")
    plt.title("Total genres: " + str(shownlens[0]) + ", Total % makeup of not shown genres: " + (str(notshownsums[0] / allsums[0]))[2:4] + "%")
    plt.show()

    disp2010 = dict(disp[1])
    mylabels = list(disp2010.keys())
    total = 0
    for num in disp2010.values():
        total += num
    percent2010 = []
    for num in disp2010.values():
        percent2010.append(num/total)
    y = np.array(percent2010)
    plt.pie(y, labels = mylabels)
    plt.suptitle("% make up of top 10 genres in 2010")
    plt.title("Total genres: " + str(shownlens[1]) + ", Total % makeup of not shown genres: " + (str(notshownsums[1] / allsums[1]))[2:4] + "%")
    plt.show()

    disp2020 = dict(disp[2])
    mylabels = list(disp2020.keys())
    total = 0
    for num in disp2020.values():
        total += num
    percent2020 = []
    for num in disp2020.values():
        percent2020.append(num/total)
    y = np.array(percent2020)
    plt.pie(y, labels = mylabels)
    plt.suptitle("% make up of top 10 genres in 2020")
    plt.title("Total genres: " + str(shownlens[2]) + ", Total % makeup of not shown genres: " + (str(notshownsums[2] / allsums[2]))[2:4] + "%")
    plt.show()

#making bar charts for the frequency of appearances in the top 100
def artist_bars(sumli):
    y = 0
    years = ["2000", "2010", "2020"]
    for year in years:
        plt.style.use('ggplot')

        x = list((sumli[y][-1]).keys())
        energy = list((sumli[y][-1]).values())

        x_pos = [i for i, _ in enumerate(x)]

        plt.bar(x_pos, energy, color='green')
        plt.xlabel("#of times artist appeared")
        plt.ylabel("#of occurences")
        plt.title("Number of times artists appeared x number of times in " + year)

        plt.xticks(x_pos, x)
        y += 1
        plt.show()

def main():
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()
    #making the tables with spotify info 

    cur.execute("CREATE TABLE IF NOT EXISTS billboard2000 ('id' TEXT PRIMARY KEY, 'track' TEXT, 'artist' TEXT, 'genres' TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS billboard2010 ('id' TEXT PRIMARY KEY, 'track' TEXT, 'artist' TEXT, 'genres' TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS billboard2020 ('id' TEXT PRIMARY KEY, 'track' TEXT, 'artist' TEXT, 'genres' TEXT)")
    
    cur.execute("SELECT COUNT('id') FROM billboard2000")
    count2000 = cur.fetchall()

    if int(count2000[0][0]) >= 100:
        print("Spotify Scraping Complete")

        #--CALCULATIONS--
        artist_frequency()
        sumli = year_analysis()
        
        #--VISUALIZATIONS--
        audio_lines(sumli)
        genre_pies(sumli)
        artist_bars(sumli)
        conn.commit()
    else:
        spotify_tables(count2000)
        

if __name__ == "__main__":
    main()
