# Final Project - Top 100 Music 2000
# By: Nathan Witt, Anders Lundin, Ryan Horlick

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

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
        rank = int((song.find_all('td'))[0].text)
        song_dict[rank] = {}
        links = song.find_all('a')
        song_dict[rank]['song_name'] = links[0].text
        song_dict[rank]['artist'] = links[1].text

    return song_dict

def main():

    # test on year 2020
    print(scrape_top_music(2020))

if __name__ == "__main__":
    main()

    



