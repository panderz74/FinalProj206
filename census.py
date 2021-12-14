# SI 206 Final Project
# Census API

import matplotlib
import requests
import json
import sqlite3
import ast
import matplotlib.pyplot as plt
import numpy as np

def run(link):
    resp = requests.get(link)
    return ast.literal_eval(resp.text)

# Line chart demonstrating US Population Diversity by Race in years 2000, 2010, 2020
def viz(pli):
    africanAmerican = np.array([pli[0][1], pli[1][1], pli[2][1]])
    hispanicLatinoy1 = np.array([pli[0][5], pli[1][5], pli[2][5]])
    twoOrMoreRacesy2 = np.array([pli[0][6], pli[1][6], pli[2][6]])
    whitey3 = np.array([pli[0][0], pli[1][0], pli[2][0]])
    other = np.array([(pli[0][2] + pli[0][4]), (pli[1][2] + pli[1][4]), (pli[2][2] + pli[2][4])])
    years = ["2000", "2010", "2020"]

    plt.title("US Population Diversity by Race Over Time")
    plt.xlabel("Year")
    plt.ylabel("Percentage")

    plt.plot(years, whitey3, "-b", label = "White")
    plt.plot(years, twoOrMoreRacesy2, "-g", label = "Two Or More Races")
    plt.plot(years, hispanicLatinoy1, "-r", label = "Hispanic or Latino")
    plt.plot(years, africanAmerican, "-y", label = "Black or African American")
    plt.plot(years, other, "-o", label = "Other")

    plt.legend(loc="upper right")

    plt.show()

def viz2(pli):
    # Pie Chart demonstrating US Population Diversity Percentages by Race in 2000
    labels = 'White', 'AfricanAmerican', 'Asian', 'Hispanic or Latino', 'Two or More Races', 'Other'
    sizes = [pli[0][0], pli[0][1], pli[0][3], pli[0][5], pli[0][6], (pli[0][2] + pli[0][4])]
    colors = ['blue', 'yellow', 'green', 'brown', 'purple', 'orange']

    plt.suptitle("US Population Diversity by Race in 2000")
    plt.title("Other = PacificIslander, American Indian, Alaska & Hawaiian Native")

    plt.pie(sizes, labels=labels, colors=colors, shadow=False, startangle=140)

    plt.axis('equal')
    plt.show()

    # Pie Chart demonstrating US Population Diversity Percentages by Race in 2010
    labels = 'White', 'AfricanAmerican', 'Asian', 'Hispanic or Latino', 'Two or More Races', 'Other'
    sizes = [pli[1][0], pli[1][1], pli[1][3], pli[1][5], pli[1][6], (pli[1][2] + pli[1][4])]
    colors = ['blue', 'yellow', 'green', 'brown', 'purple', 'orange']

    plt.suptitle("US Population Diversity by Race in 2010")
    plt.title("Other = PacificIslander, American Indian, Alaska & Hawaiian Native")

    plt.pie(sizes, labels=labels, colors=colors, shadow=False, startangle=140)

    plt.axis('equal')
    plt.show()

    # Pie Chart demonstrating US Population Diversity Percentages by Race in 2020
    labels = 'White', 'AfricanAmerican', 'Asian', 'Hispanic or Latino', 'Two or More Races', 'Other'
    sizes = [pli[2][0], pli[2][1], pli[2][3], pli[2][5], pli[2][6], (pli[2][2] + pli[2][4])]
    colors = ['blue', 'yellow', 'green', 'brown', 'purple', 'orange']

    plt.suptitle("US Population Diversity by Race in 2020")
    plt.title("Other = PacificIslander, American Indian, Alaska & Hawaiian Native")

    plt.pie(sizes, labels=labels, colors=colors, shadow=False)

    plt.axis('equal')
    plt.show()

def write_file():
    d2000 = {}
    d2010 = {}
    d2020 = {}
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()
    # Total White Population Over Time
    
    cur.execute('SELECT SUM (White) FROM census2000')
    white2000 = cur.fetchall()
    d2000["White2000"] = white2000[0][0]

    cur.execute('SELECT SUM(White) FROM census2010')
    white2010 = cur.fetchall()
    d2010["White2010"] = white2010[0][0]

    cur.execute('SELECT SUM(White) FROM census2020')
    white2020 = cur.fetchall()
    d2020["White2020"] = white2020[0][0]

    # Total AfricanAmerican Population Over Time

    cur.execute('SELECT SUM(AfricanAmerican) FROM census2000')
    africanAmerican2000 = cur.fetchall()
    d2000["AfricanAmerican2000"] = africanAmerican2000[0][0]

    cur.execute('SELECT SUM(AfricanAmerican) FROM census2010')
    africanAmerican2010 = cur.fetchall()
    d2010["AfricanAmerican2010"] = africanAmerican2010[0][0]

    cur.execute('SELECT SUM(AfricanAmerican) FROM census2020')
    africanAmerican2020 = cur.fetchall()
    d2020["AfricanAmerican2020"] = africanAmerican2020[0][0]

    # Total AmericanIndianAlaska Population Over Time

    cur.execute('SELECT SUM(AmericanIndianAlaska) FROM census2000')
    americanIndianAlaska2000 = cur.fetchall()
    d2000["AmericanIndianAlaska2000"] = americanIndianAlaska2000[0][0]

    cur.execute('SELECT SUM(AmericanIndianAlaska) FROM census2010')
    americanIndianAlaska2010 = cur.fetchall()
    d2010["AmericanIndianAlaska2010"] = americanIndianAlaska2010[0][0]

    cur.execute('SELECT SUM(AmericanIndianAlaska) FROM census2020')
    americanIndianAlaska2020 = cur.fetchall()
    d2020["AmericanIndianAlaska2020"] = americanIndianAlaska2020[0][0]

    # Total Asian Population Over Time

    cur.execute('SELECT SUM(Asian) FROM census2000')
    asian2000 = cur.fetchall()
    d2000["Asian2000"] = asian2000[0][0]

    cur.execute('SELECT SUM(Asian) FROM census2010')
    asian2010 = cur.fetchall()
    d2010["Asian2010"] = asian2010[0][0]

    cur.execute('SELECT SUM(Asian) FROM census2020')
    asian2020 = cur.fetchall()
    d2020["Asian2020"] = asian2020[0][0]

    # Total HawaiianOtherPacificIslander Population Over Time

    cur.execute('SELECT SUM(HawaiianOtherPacificIslander) FROM census2000')
    hawaiianOtherPacificIslander2000 = cur.fetchall()
    d2000["HawaiianOtherPacificIslander2000"] = hawaiianOtherPacificIslander2000[0][0]

    cur.execute('SELECT SUM(HawaiianOtherPacificIslander) FROM census2010')
    hawaiianOtherPacificIslander2010 = cur.fetchall()
    d2010["HawaiianOtherPacificIslander2010"] = hawaiianOtherPacificIslander2010[0][0]

    cur.execute('SELECT SUM(HawaiianOtherPacificIslander) FROM census2020')
    hawaiianOtherPacificIslander2020 = cur.fetchall()
    d2020["HawaiianOtherPacificIslander2020"] = hawaiianOtherPacificIslander2020[0][0]

    # Total HispanicLatino Population Over Time

    cur.execute('SELECT SUM(HispanicLatino) FROM census2000')
    hispanicLatino2000 = cur.fetchall()
    d2000["HispanicLatino2000"] = hispanicLatino2000[0][0]

    cur.execute('SELECT SUM(HispanicLatino) FROM census2010')
    hispanicLatino2010 = cur.fetchall()
    d2010["HispanicLatino2010"] = hispanicLatino2010[0][0]

    cur.execute('SELECT SUM(HispanicLatino) FROM census2020')
    hispanicLatino2020 = cur.fetchall()
    d2020["HispanicLatino2020"] = hispanicLatino2020[0][0]

    # Total TwoOrMoreRaces Population Over Time

    cur.execute('SELECT SUM(TwoOrMoreRaces) FROM census2000')
    twoOrMoreRaces2000 = cur.fetchall()
    d2000["TwoOrMoreRaces2000"] = twoOrMoreRaces2000[0][0]

    cur.execute('SELECT SUM(TwoOrMoreRaces) FROM census2010')
    twoOrMoreRaces2010 = cur.fetchall()
    d2010["TwoOrMoreRaces2010"] = twoOrMoreRaces2010[0][0]

    cur.execute('SELECT SUM(TwoOrMoreRaces) FROM census2020')
    twoOrMoreRaces2020 = cur.fetchall()
    d2020["TwoOrMoreRaces2020"] = twoOrMoreRaces2020[0][0]

    tot_pops =[d2000, d2010, d2020]

    f= open("documentation.txt", "+a")
    f.write("\n\n\nPopulation Totals for 2000:\n")
    f.write("Total White Population: " + str(white2000[0][0]) + "\n")
    f.write("Total African American Population: " + str(africanAmerican2000[0][0]) + "\n")
    f.write("Total American Indian Alaskan Population: " + str(americanIndianAlaska2000[0][0]) + "\n")
    f.write("Total Asian Population: " + str(asian2000[0][0]) + "\n")
    f.write("Total Hawaiian and Other Pacific Islander Population: " + str(hawaiianOtherPacificIslander2000[0][0]) + "\n")
    f.write("Total Hispanic / Latino Population: " + str(hispanicLatino2000[0][0]) + "\n")
    f.write("Total Two or More Races Population: " + str(twoOrMoreRaces2000[0][0]) + "\n")

    f.write("\n\nPopulation Totals for 2010:\n")
    f.write("Total White Population: " + str(white2010[0][0]) + "\n")
    f.write("Total African American Population: " + str(africanAmerican2010[0][0]) + "\n")
    f.write("Total American Indian Alaskan Population: " + str(americanIndianAlaska2010[0][0]) + "\n")
    f.write("Total Asian Population: " + str(asian2010[0][0]) + "\n")
    f.write("Total Hawaiian and Other Pacific Islander Population: " + str(hawaiianOtherPacificIslander2010[0][0]) + "\n")
    f.write("Total Hispanic / Latino Population: " + str(hispanicLatino2010[0][0]) + "\n")
    f.write("Total Two or More Races Population: " + str(twoOrMoreRaces2010[0][0]) + "\n")

    f.write("\n\nPopulation Totals for 2020:\n")
    f.write("Total White Population: " + str(white2020[0][0]) + "\n")
    f.write("Total African American Population: " + str(africanAmerican2020[0][0]) + "\n")
    f.write("Total American Indian Alaskan Population: " + str(americanIndianAlaska2020[0][0]) + "\n")
    f.write("Total Asian Population: " + str(asian2020[0][0]) + "\n")
    f.write("Total Hawaiian and Other Pacific Islander Population: " + str(hawaiianOtherPacificIslander2020[0][0]) + "\n")
    f.write("Total Hispanic / Latino Population: " + str(hispanicLatino2020[0][0]) + "\n")
    f.write("Total Two or More Races Population: " + str(twoOrMoreRaces2020[0][0]) + "\n")

    f.close()
    conn.commit()

    return(tot_pops)


def writepercents(totli):
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()

    totalPopulation2000 = 0
    totalPopulation2010 = 0
    totalPopulation2020 = 0
    for num in totli[0].values():
        totalPopulation2000 += num
    
    for num in totli[1].values():
        totalPopulation2010 += num

    for num in totli[2].values():
        totalPopulation2020 += num
    
    # White Percentage of the US Population 2000-2020

    whitePercentage2000 = totli[0]["White2000"] / totalPopulation2000 
    whitePercentage2010 = totli[1]["White2010"] / totalPopulation2010
    whitePercentage2020 = totli[2]["White2020"] / totalPopulation2020

    # African American Percentage of the US Population 2000-2020
    africanamericanPercentage2000 = totli[0]["AfricanAmerican2000"] / totalPopulation2000 
    africanamericanPercentage2010 = totli[1]["AfricanAmerican2010"] / totalPopulation2010
    africanamericanPercentage2020 = totli[2]["AfricanAmerican2020"] / totalPopulation2020

    # AmericanIndianAlaska Percentage of the US Population 2000-2020
    americanIndianAlaskaPercentage2000 = totli[0]["AmericanIndianAlaska2000"] / totalPopulation2000 
    americanIndianAlaskaPercentage2010 = totli[1]["AmericanIndianAlaska2010"] / totalPopulation2010
    americanIndianAlaskaPercentage2020 = totli[2]["AmericanIndianAlaska2020"] / totalPopulation2020

    # Asian Percentage of the US Population 2000-2020
    asianPercentage2000 = totli[0]["Asian2000"] / totalPopulation2000 
    asianPercentage2010 = totli[1]["Asian2010"] / totalPopulation2010
    asianPercentage2020 = totli[2]["Asian2020"] / totalPopulation2020

    # HawaiianOtherPacificIslander Percentage of the US Population 2000-2020
    hawaiianOtherPacificIslanderPercentage2000 = totli[0]["HawaiianOtherPacificIslander2000"] / totalPopulation2000 
    hawaiianOtherPacificIslanderPercentage2010 = totli[1]["HawaiianOtherPacificIslander2010"] / totalPopulation2010
    hawaiianOtherPacificIslanderPercentage2020 = totli[2]["HawaiianOtherPacificIslander2020"] / totalPopulation2020

    # HispanicLatino Percentage of the US Population 2000-2020
    hispanicLatinoPercentage2000 = totli[0]["HispanicLatino2000"] / totalPopulation2000 
    hispanicLatinoPercentage2010 = totli[1]["HispanicLatino2010"] / totalPopulation2010
    hispanicLatinoPercentage2020 = totli[2]["HispanicLatino2020"] / totalPopulation2020

    # TwoOrMoreRaces Percentage of the US Population 2000-2020
    twoOrMoreRacesPercentage2000 = totli[0]["TwoOrMoreRaces2000"] / totalPopulation2000 
    twoOrMoreRacesPercentage2010 = totli[1]["TwoOrMoreRaces2010"] / totalPopulation2010
    twoOrMoreRacesPercentage2020 = totli[2]["TwoOrMoreRaces2020"] / totalPopulation2020

    p2000 = [whitePercentage2000, africanamericanPercentage2000, americanIndianAlaskaPercentage2000, asianPercentage2000, hawaiianOtherPacificIslanderPercentage2000, hispanicLatinoPercentage2000, twoOrMoreRacesPercentage2000]
    p2010 = [whitePercentage2010, africanamericanPercentage2010, americanIndianAlaskaPercentage2010, asianPercentage2010, hawaiianOtherPacificIslanderPercentage2010, hispanicLatinoPercentage2010, twoOrMoreRacesPercentage2010]
    p2020 = [whitePercentage2020, africanamericanPercentage2020, americanIndianAlaskaPercentage2020, asianPercentage2020, hawaiianOtherPacificIslanderPercentage2020, hispanicLatinoPercentage2020, twoOrMoreRacesPercentage2020]

    f = open("documentation.txt", "a+")
    f.write("\n\nTotal percent makeup of each race by year: \n")
    f.write("White 2000: " + str(whitePercentage2000) + "\n")
    f.write("White 2010: " + str(whitePercentage2010) + "\n")
    f.write("White 2020: " + str(whitePercentage2020) + "\n")
    f.write("African American 2000: " + str(africanamericanPercentage2000) + "\n")
    f.write("African American 2010: " + str(africanamericanPercentage2010) + "\n")
    f.write("African American 2020: " + str(africanamericanPercentage2020) + "\n")
    f.write("American Indian Alaska 2000: " + str(americanIndianAlaskaPercentage2000) + "\n")
    f.write("American Indian Alaska 2010: " + str(americanIndianAlaskaPercentage2010) + "\n")
    f.write("American Indian Alaska 2020: " + str(americanIndianAlaskaPercentage2020) + "\n")
    f.write("Asian 2000: " + str(asianPercentage2000) + "\n")
    f.write("Asian 2010: " + str(asianPercentage2010) + "\n")
    f.write("Asian 2020: " + str(asianPercentage2020) + "\n")
    f.write("Hawaiian / Other Pacific Islanders 2000: " + str(hawaiianOtherPacificIslanderPercentage2000) + "\n")
    f.write("Hawaiian / Other Pacific Islanders 2010: " + str(hawaiianOtherPacificIslanderPercentage2010) + "\n")
    f.write("Hawaiian / Other Pacific Islanders 2020: " + str(hawaiianOtherPacificIslanderPercentage2020) + "\n")
    f.write("Hispanic / Latino 2000: " + str(hispanicLatinoPercentage2000) + "\n")
    f.write("Hispanic / Latino 2010: " + str(hispanicLatinoPercentage2010) + "\n")
    f.write("Hispanic / Latino 2020: " + str(hispanicLatinoPercentage2020) + "\n")
    f.write("Two or More Races 2000: " + str(twoOrMoreRacesPercentage2000) + "\n")
    f.write("Two or More Races 2010: " + str(twoOrMoreRacesPercentage2010) + "\n")
    f.write("Two or More Races 2020: " + str(twoOrMoreRacesPercentage2020) + "\n\n")
    
    f.close()
    conn.commit()
    return([p2000, p2010, p2020])

def main():
    f= open("documentation.txt", "a+")

    # Creates census database and provides column labels
    conn = sqlite3.connect('charts.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS census2000 ('State_Name' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS census2010 ('State_Name' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS census2020 ('State_Name' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")

    state_list = ['01','02','04','05','06','08','09','10','11','12','13','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','41','42','44','45','46','47','48','49','50','51','53','54','55', '56']
    states = ""

    # Finds index of next state to add from 2000 Census
    cur.execute("SELECT COUNT('State_Name') FROM census2000")
    count2000 = cur.fetchall()
    count2000 = int(count2000[0][0])

    # Checks if all Census data has been gathered yet
    if count2000 >= 50:
        print("Census Scraping Complete")
        view = writepercents(write_file())
        viz(view)
        viz2(view)

    else:
        # Processes the next 25 states to add from Census 2000 and runs the API
        for i in state_list[count2000:count2000+25]:
            states += (i + ",")
        states = states.rstrip(",")
        resp2000 = run("https://api.census.gov/data/2000/dec/sf1?get=NAME,P003003,P003004,P003005,P003006,P003007,P004002,P003009&for=state:" + states + "&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b")
        
        # Finds index of next state to add from 2010 Census
        cur.execute("SELECT COUNT('State_Name') FROM census2010")
        count2010 = cur.fetchall()
        count2010 = int(count2010[0][0])

        # Processes the next 25 states to add from Census 2000 and runs the API
        for i in state_list[count2010:count2010+25]:
            states += (i + ",")
        states = states.rstrip(",")
        resp2010 = run("https://api.census.gov/data/2010/dec/sf1?get=NAME,P008003,P008004,P008005,P008006,P008007,P005010,P008009&for=state:" + states + "&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b")

        # Finds index of next state to add from 2020 Census
        cur.execute("SELECT COUNT('State_Name') FROM census2020")
        count2020 = cur.fetchall()
        count2020 = int(count2020[0][0])

        # Processes the next 25 states to add from Census 2000 and runs the API
        for i in state_list[count2020:count2020+25]:
            states += (i + ",")
        states = states.rstrip(",")
        resp2020 = run("https://api.census.gov/data/2020/dec/pl?get=NAME,P1_003N,P1_004N,P1_005N,P1_006N,P1_007N,P2_002N,P1_009N&for=state:" + states + "&key=fefbbcd5f615aedd630f43ad9e5331e83ae4982b")

        # Loops through the API results for all three years and stores it three respective tables
        for d in resp2000[1:]:
            cur.execute('INSERT INTO census2000 (State_Name, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
        for d in resp2010[1:]:
            cur.execute('INSERT INTO census2010 (State_Name, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
        for d in resp2020[1:]:
            cur.execute('INSERT INTO census2020 (State_Name, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))

        conn.commit()




if __name__ == "__main__":
    main()