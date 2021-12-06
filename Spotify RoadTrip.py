import json
import unittest
import os
import requests
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import random

CLIENT_ID = '3d63895403d14aa7833edba57df85660'
CLIENT_SECRET = '1dd33174539444ec9046878a0368ec87'
AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)

sp = spotipy.Spotify(auth_manager=auth_manager)

cities = {"owensboro": "69CLtpNTiudT6yjju9hffn", "hollywood": "3WUq5A66fjNKyQhOuXec5A", "lasvegas":"2CXkeGUXvtOzxTMPmMyZpm", 
    "jackson":"52XXLFkh6oti95F21bkgs", "austin":"5rJr4W7o4vk1GWzJqEnEYO", "minneapolis": "43wIofeoTF1BFcpsl0lxEq",
    "sanfrancisco":"2fVERTIYwT9XxMP5HdGb84", "cheyenne":"2Dw4KeILTFJxbySF0U35oG", "charleston":"1RpSEm06WWBDIXpXj1ovm2",
    "milwaukee":"3gomz6VxrOo7uzksBAlv3p", "cleveland":"0L2mzWTT1tCSmHGlD4Msod", "siouxfalls":"53e6A5DAqS4MXKVXQUDBJ6",
    "sanantonio": "5ONgmu3SeZ9zoEdbUoqy5k", "providence":"39uaUYL0DrQ5TlCdMdw5tg", "baltimore":"1ADXInRe1YbFBLCeEJHxso",
    "denver":"3ML5VjtU3OTnAEyI3CJqRu", "atlanta":"0EYAhhOn0wNmMHDPFPky0j", "houston":"07rkeMKsZKRuIDbpQYCWqT",
    "portland":"2BclOG0iN6Qusls1AHku0T", "nashville": "5nD7S1Z17IPodw2KjYynyy", "neworleans": "68gsLy06VRcGEytFxFy7WT",
    "detroit":"4Zn4kjShlGYhDLz0dVpGBp", "losangeles":"3PQaecBEegMAdK0Uv6p54T", "memphis":"3JsqfItBrSgbzkJsJXyHNd",
    "chicago":"5hTmfOuMKTC3w1Zpq5hFcQ", "nyc":"12DnDaFQDkgbZd5B0AihFR", "miami":"7aqunQuY5WvhOCimcQbEx5"}

#returns id, song name, album, artist of each song on playlist
def playlistsongs(id):
    plist = sp.playlist_tracks(id)
    listinfo = []
    for song in plist["items"]:
        songdict = {}
        songdict["id"] = song["track"]["id"]
        songdict["song"] = song["track"]["name"]
        songdict["album"] = song["track"]["album"]["name"]
        songdict["artist"] = song["track"]["album"]["artists"][0]["name"]
        listinfo.append(songdict)
    return listinfo

#takes a list of cities and returns a list of information for each 
def plsinfo(pls):
    pls_info = {}
    for pl in pls:
        pls_info[pl] = playlistsongs(cities[pl])
    return pls_info

outWest=["sanfrancisco", "sanantonio", "losangeles"]
western = plsinfo(outWest)

#takes a list with city playlist information and randomly selects 10 songs from each city and returns them in a list
def maketrip(pls):
    newlist = []
    for pl in pls.values():
        newlist.append(random.sample(pl,10))
    new= []
    for item in newlist:
        new = new + item
    return new

westerntrip = maketrip(western)

#takes the id from each dictionary and makes a list of ids
def getids(pl):
    newli = []
    for song in pl:
        newli.append(song["id"])
    return newli

print(westerntrip)
print(getids(westerntrip))