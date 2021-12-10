# SI 206 Final Project
# OpenWeather API
# Ryan Horlick

import requests
import json
import sqlite3
import ast

census2000 = "https://api.census.gov/data/2000/dec/sf1?get=NAME,P003003,P003004,P003005,P003006,P003007,P004002,P003009&for=state:*&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b"

census2010 = "https://api.census.gov/data/2010/dec/sf1?get=NAME,P008003,P008004,P008005,P008006,P008007,P005010,P008009&for=state:*&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b"

census2020 = "https://api.census.gov/data/2020/dec/pl?get=NAME,P1_003N,P1_004N,P1_005N,P1_006N,P1_007N,P2_002N,P1_009N&for=state:*&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b"

resp2000 = requests.get(census2000)
resp2000 = ast.literal_eval(resp2000.text)
resp2010 = requests.get(census2010)
resp2010 = ast.literal_eval(resp2010.text)
resp2020 = requests.get(census2020)
resp2020 = ast.literal_eval(resp2020.text)

def main():
    conn = sqlite3.connect('census.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS census2000")
    cur.execute("CREATE TABLE census2000 ('State' TEXT PRIMARY KEY, 'White' TEXT, 'Black/African American' TEXT, 'American Indian and Alaska Native' TEXT, 'Asian' TEXT, 'Native Hawaiian and Other Pacific Islander' TEXT, 'Hispanic or Latino' TEXT, 'Two or more races' TEXT)")
    cur.execute("DROP TABLE IF EXISTS census2010")
    cur.execute("CREATE TABLE census2010 ('State' TEXT PRIMARY KEY, 'White' TEXT, 'Black/African American' TEXT, 'American Indian and Alaska Native' TEXT, 'Asian' TEXT, 'Native Hawaiian and Other Pacific Islander' TEXT, 'Hispanic or Latino' TEXT, 'Two or more races' TEXT)")
    cur.execute("DROP TABLE IF EXISTS census2020")
    cur.execute("CREATE TABLE census2020 ('State' TEXT PRIMARY KEY, 'White' TEXT, 'Black/African American' TEXT, 'American Indian and Alaska Native' TEXT, 'Asian' TEXT, 'Native Hawaiian and Other Pacific Islander' TEXT, 'Hispanic or Latino' TEXT, 'Two or more races' TEXT)")                                                                            
    
    for d in resp2000:
        cur.execute('INSERT INTO census2000 (State_Name, White, BlackAfrican American, American IndianAlaska, Asian, HawaiianOther Pacific Islander, HispanicLatino, Twomore races) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
    for d in resp2010:
        cur.execute('INSERT INTO census2010 (State_Name, White, BlackAfrican American, American IndianAlaska, Asian, HawaiianOther Pacific Islander, HispanicLatino, Twomore races) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
    for d in resp2020:
        cur.execute('INSERT INTO census2020 (State_Name, White, BlackAfrican American, American IndianAlaska, Asian, HawaiianOther Pacific Islander, HispanicLatino, Twomore races) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))

    conn.commit()