# SI 206 Final Project
# OpenWeather API
# Ryan Horlick

import requests
import json
import sqlite3
import ast

def get_2000(link):
    resp2000 = requests.get(link)
    return ast.literal_eval(resp2000.text)

def get_2010(link):
    resp2010 = requests.get(link)
    return ast.literal_eval(resp2010.text)

def get_2020(link):
    resp2020 = requests.get(link)
    return ast.literal_eval(resp2020.text)



def main():

    resp2000 = get_2000("https://api.census.gov/data/2000/dec/sf1?get=NAME,P003003,P003004,P003005,P003006,P003007,P004002,P003009&for=state:*&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b")
    resp2010 = get_2010("https://api.census.gov/data/2010/dec/sf1?get=NAME,P008003,P008004,P008005,P008006,P008007,P005010,P008009&for=state:*&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b")
    resp2020 = get_2020("https://api.census.gov/data/2020/dec/pl?get=NAME,P1_003N,P1_004N,P1_005N,P1_006N,P1_007N,P2_002N,P1_009N&for=state:*&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b")

    conn = sqlite3.connect('census.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS census2000")
    cur.execute("CREATE TABLE census2000 ('State_Name' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")
    cur.execute("DROP TABLE IF EXISTS census2010")
    cur.execute("CREATE TABLE census2010 ('State_Name' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")
    cur.execute("DROP TABLE IF EXISTS census2020")
    cur.execute("CREATE TABLE census2020 ('State_Name' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")

    for d in resp2000:
        cur.execute('INSERT INTO census2000 (State_Name, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
    for d in resp2010:
        cur.execute('INSERT INTO census2010 (State_Name, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
    for d in resp2020:
        cur.execute('INSERT INTO census2020 (State_Name, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))

    conn.commit()

    
if __name__ == "__main__":
    main()