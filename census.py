# SI 206 Final Project
# Census API

import matplotlib
import requests
import json
import sqlite3
import ast

def run(link):
    resp = requests.get(link)
    return ast.literal_eval(resp.text)

def viz():
    #### MatPlot Visualizations

    # Line chart demonstrating US Population Diversity by Race in years 2000, 2010, 2020
    import matplotlib.pyplot as plt
    import numpy as np
    
    AfricanAmerican = np.array([.11, .11, .11])
    HispanicLatinoy1 = np.array([.13, .16, .18])
    TwoOrMoreRacesy2 = np.array([.02, .028, .096])
    Whitey3 = np.array([.67, .63, .53])
    Other = np.array([.07, .072, .084])
    years = ["2000", "2010", "2020"]

    plt.title("US Population Diversity by Race Over Time")
    plt.xlabel("Year")
    plt.ylabel("Percentage")

    plt.plot(years, Whitey3, "-b", label = "White")
    plt.plot(years, TwoOrMoreRacesy2, "-g", label = "Two Or More Races")
    plt.plot(years, HispanicLatinoy1, "-r", label = "Hispanic or Latino")
    plt.plot(years, AfricanAmerican, "-y", label = "Black or African American")
    plt.plot(years, Other, "-o", label = "Other")

    plt.legend(loc="upper right")

    plt.show()

    # Pie Chart demonstrating US Population Diversity Percentages by Race in 2000
    labels = 'White', 'AfricanAmerican', 'Asian', 'Hispanic or Latino', 'Two or More Races', 'Other'
    sizes = [.67, .114, .03, .13, .02, 0.00922144568]
    colors = ['blue', 'yellow', 'green', 'brown', 'purple', 'orange']

    plt.suptitle("US Population Diversity by Race in 2000")
    plt.title("Other = PacificIslander, American Indian, Alaska & Hawaiian Native")

    plt.pie(sizes, labels=labels, colors=colors, shadow=False, startangle=140)

    plt.axis('equal')
    plt.show()

    # Pie Chart demonstrating US Population Diversity Percentages by Race in 2010
    labels = 'White', 'AfricanAmerican', 'Asian', 'Hispanic or Latino', 'Two or More Races', 'Other'
    sizes = [.63, .117, .05, .16, .028, 0.0096857384]
    colors = ['blue', 'yellow', 'green', 'brown', 'purple', 'orange']

    plt.suptitle("US Population Diversity by Race in 2010")
    plt.title("Other = PacificIslander, American Indian, Alaska & Hawaiian Native")

    plt.pie(sizes, labels=labels, colors=colors, shadow=False, startangle=140)

    plt.axis('equal')
    plt.show()

    # Pie Chart demonstrating US Population Diversity Percentages by Race in 2020
    labels = 'White', 'AfricanAmerican', 'Asian', 'Hispanic or Latino', 'Two or More Races', 'Other'
    sizes = [.53, .116, .061, .18, .096, 0.0119475867]
    colors = ['blue', 'yellow', 'green', 'brown', 'purple', 'orange']

    plt.suptitle("US Population Diversity by Race in 2020")
    plt.title("Other = PacificIslander, American Indian, Alaska & Hawaiian Native")

    plt.pie(sizes, labels=labels, colors=colors, shadow=False)

    plt.axis('equal')
    plt.show()

    return 

def main():

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
        viz()
        

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

        # All Below calculations aggregate population totals by race from census.db -- census2000
        
        # Total Number of White Individuals in 2000
        total_White_2000 = 0

        for d in resp2000[1:]:
            total_White_2000 = total_White_2000 + int(d[1])

        # Total Number of African American Individuals in 2000
        total_AfricanAmerican_2000 = 0
        
        for d in resp2000[1:]:
            total_AfricanAmerican_2000 = total_AfricanAmerican_2000 + int(d[2])

        # Total Number of American Indian and Alaska Native Individuals in 2000
        total_AmericanIndianAlaska_2000 = 0
        
        for d in resp2000[1:]:
            total_AmericanIndianAlaska_2000 = total_AmericanIndianAlaska_2000 + int(d[3])

        # Total Number of Asian Individuals in 2000
        total_Asian_2000 = 0
        
        for d in resp2000[1:]:
            total_Asian_2000 = total_Asian_2000 + int(d[4])

        # Total Number of Hawaiian Natives and Paicfic Islander Individuals in 2000
        total_HawaiianOtherPacificIslander_2000  = 0
        
        for d in resp2000[1:]:
            total_HawaiianOtherPacificIslander_2000 = total_HawaiianOtherPacificIslander_2000 + int(d[5])

        # Total Number of Hispanic or Latino Individuals in 2000
        total_HispanicLatino_2000 = 0
        
        for d in resp2000[1:]:
            total_HispanicLatino_2000 = total_HispanicLatino_2000 + int(d[6])

        # Total Number of Two or More Race Individuals in 2000
        total_TwoOrMoreRaces_2000 = 0
        
        for d in resp2000[1:]:
            total_TwoOrMoreRaces_2000 = total_TwoOrMoreRaces_2000 + int(d[7])

        # All Below calculations aggregate population totals by race from census.db -- census2010

        # Total Number of White Individuals in 2010
        total_White_2010 = 0

        for d in resp2010[1:]:
            total_White_2010 = total_White_2010 + int(d[1])

        # Total Number of African American Individuals in 2010
        total_AfricanAmerican_2010 = 0
        
        for d in resp2010[1:]:
            total_AfricanAmerican_2010 = total_AfricanAmerican_2010 + int(d[2])

        # Total Number of American Indian and Alaska Native Individuals in 2010
        total_AmericanIndianAlaska_2010 = 0
        
        for d in resp2010[1:]:
            total_AmericanIndianAlaska_2010 = total_AmericanIndianAlaska_2010 + int(d[3])

        # Total Number of Asian Individuals in 2010
        total_Asian_2010 = 0
        
        for d in resp2010[1:]:
            total_Asian_2010 = total_Asian_2010 + int(d[4])

        # Total Number of Hawaiian Natives and Paicfic Islander Individuals in 2010
        total_HawaiianOtherPacificIslander_2010  = 0
        
        for d in resp2010[1:]:
            total_HawaiianOtherPacificIslander_2010 = total_HawaiianOtherPacificIslander_2010 + int(d[5])

        # Total Number of Hispanic or Latino Individuals in 2010
        total_HispanicLatino_2010 = 0
        
        for d in resp2010[1:]:
            total_HispanicLatino_2010 = total_HispanicLatino_2010 + int(d[6])

        # Total Number of Two or More Race Individuals in 2010
        total_TwoOrMoreRaces_2010 = 0
        
        for d in resp2010[1:]:
            total_TwoOrMoreRaces_2010 = total_TwoOrMoreRaces_2010 + int(d[7])

        # All Below calculations aggregate population totals by race from census.db -- census2020

        # Total Number of White Individuals in 2020
        total_White_2020 = 0

        for d in resp2020[1:]:
            total_White_2020 = total_White_2020 + int(d[1])

        # Total Number of African American Individuals in 2020
        total_AfricanAmerican_2020 = 0
        
        for d in resp2020[1:]:
            total_AfricanAmerican_2020 = total_AfricanAmerican_2020 + int(d[2])

        # Total Number of American Indian and Alaska Native Individuals in 2020
        total_AmericanIndianAlaska_2020 = 0
        
        for d in resp2020[1:]:
            total_AmericanIndianAlaska_2020 = total_AmericanIndianAlaska_2020 + int(d[3])

        # Total Number of Asian Individuals in 2020
        total_Asian_2020 = 0
        
        for d in resp2020[1:]:
            total_Asian_2020 = total_Asian_2020 + int(d[4])

        # Total Number of Hawaiian Natives and Paicfic Islander Individuals in 2020
        total_HawaiianOtherPacificIslander_2020  = 0
        
        for d in resp2020[1:]:
            total_HawaiianOtherPacificIslander_2020 = total_HawaiianOtherPacificIslander_2020 + int(d[5])

        # Total Number of Hispanic or Latino Individuals in 2020
        total_HispanicLatino_2020 = 0
        
        for d in resp2020[1:]:
            total_HispanicLatino_2020 = total_HispanicLatino_2020 + int(d[6])

        # Total Number of Two or More Race Individuals in 2020
        total_TwoOrMoreRaces_2020 = 0
        
        for d in resp2020[1:]:
            total_TwoOrMoreRaces_2020 = total_TwoOrMoreRaces_2020 + int(d[7])

        
        # Inserts tables for diversity totals in US during 2000, 2010, and 2020, in order to organizen the calculations conducted above. NOT API-pulled data so no later data extractions were made. This is purely a summary / reference 
        cur.execute("DROP TABLE IF EXISTS censustotal2000")
        cur.execute("CREATE TABLE censustotal2000 ('Year' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")
        cur.execute("DROP TABLE IF EXISTS censustotal2010")
        cur.execute("CREATE TABLE censustotal2010 ('Year' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")
        cur.execute("DROP TABLE IF EXISTS censustotal2020")
        cur.execute("CREATE TABLE censustotal2020 ('Year' TEXT PRIMARY KEY, 'White' TEXT, 'AfricanAmerican' TEXT, 'AmericanIndianAlaska' TEXT, 'Asian' TEXT, 'HawaiianOtherPacificIslander' TEXT, 'HispanicLatino' TEXT, 'TwoOrMoreRaces' TEXT)")


        cur.execute('INSERT INTO censustotal2000 (Year, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', ('2000', total_White_2000, total_AfricanAmerican_2000, total_AmericanIndianAlaska_2000, total_Asian_2000, total_HawaiianOtherPacificIslander_2000, total_HispanicLatino_2000, total_TwoOrMoreRaces_2000))
        cur.execute('INSERT INTO censustotal2010 (Year, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', ('2010', total_White_2010, total_AfricanAmerican_2010, total_AmericanIndianAlaska_2010, total_Asian_2010, total_HawaiianOtherPacificIslander_2010, total_HispanicLatino_2010, total_TwoOrMoreRaces_2010))
        cur.execute('INSERT INTO censustotal2020 (Year, White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces) VALUES (?,?,?,?,?,?,?,?)', ('2020', total_White_2020, total_AfricanAmerican_2020, total_AmericanIndianAlaska_2020, total_Asian_2020, total_HawaiianOtherPacificIslander_2020, total_HispanicLatino_2020, total_TwoOrMoreRaces_2020))
        

        conn.commit()

        # Total White Population Over Time
        
        cur.execute('SELECT SUM(White) FROM census2000')
        White2000 = cur.fetchall()

        cur.execute('SELECT SUM(White) FROM census2010')
        White2010 = cur.fetchall()

        cur.execute('SELECT SUM(White) FROM census2020')
        White2020 = cur.fetchall()

        # Total AfricanAmerican Population Over Time

        cur.execute('SELECT SUM(AfricanAmerican) FROM census2000')
        AfricanAmerican2000 = cur.fetchall()

        cur.execute('SELECT SUM(AfricanAmerican) FROM census2010')
        AfricanAmerican2010 = cur.fetchall()

        cur.execute('SELECT SUM(AfricanAmerican) FROM census2020')
        AfricanAmerican2020 = cur.fetchall()

        # Total AmericanIndianAlaska Population Over Time

        cur.execute('SELECT SUM(AmericanIndianAlaska) FROM census2000')
        AmericanIndianAlaska2000 = cur.fetchall()

        cur.execute('SELECT SUM(AmericanIndianAlaska) FROM census2010')
        AmericanIndianAlaska2010 = cur.fetchall()

        cur.execute('SELECT SUM(AmericanIndianAlaska) FROM census2020')
        AmericanIndianAlaska2020 = cur.fetchall()

        # Total Asian Population Over Time

        cur.execute('SELECT SUM(Asian) FROM census2000')
        Asian2000 = cur.fetchall()

        cur.execute('SELECT SUM(Asian) FROM census2010')
        Asian2010 = cur.fetchall()

        cur.execute('SELECT SUM(Asian) FROM census2020')
        Asian2020 = cur.fetchall()

        # Total HawaiianOtherPacificIslander Population Over Time

        cur.execute('SELECT SUM(HawaiianOtherPacificIslander) FROM census2000')
        HawaiianOtherPacificIslander2000 = cur.fetchall()

        cur.execute('SELECT SUM(HawaiianOtherPacificIslander) FROM census2010')
        HawaiianOtherPacificIslander2010 = cur.fetchall()

        cur.execute('SELECT SUM(HawaiianOtherPacificIslander) FROM census2020')
        HawaiianOtherPacificIslander2020 = cur.fetchall()

        # Total HispanicLatino Population Over Time

        cur.execute('SELECT SUM(HispanicLatino) FROM census2000')
        HispanicLatino2000 = cur.fetchall()

        cur.execute('SELECT SUM(HispanicLatino) FROM census2010')
        HispanicLatino2010 = cur.fetchall()

        cur.execute('SELECT SUM(HispanicLatino) FROM census2020')
        HispanicLatino2020 = cur.fetchall()

        # Total TwoOrMoreRaces Population Over Time

        cur.execute('SELECT SUM(TwoOrMoreRaces) FROM census2000')
        TwoOrMoreRaces2000 = cur.fetchall()

        cur.execute('SELECT SUM(TwoOrMoreRaces) FROM census2010')
        TwoOrMoreRaces2010 = cur.fetchall()

        cur.execute('SELECT SUM(TwoOrMoreRaces) FROM census2020')
        TwoOrMoreRaces2020 = cur.fetchall()


        # Total Numbers from all Races Over Time (to be entered into the database)

        cur.execute('SELECT White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces, White+AfricanAmerican+AmericanIndianAlaska+Asian+HawaiianOtherPacificIslander+HispanicLatino+TwoOrMoreRaces FROM censustotal2000')
        totalRaces2000 = cur.fetchall()


        cur.execute('SELECT White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces, White+AfricanAmerican+AmericanIndianAlaska+Asian+HawaiianOtherPacificIslander+HispanicLatino+TwoOrMoreRaces FROM censustotal2010')
        totalRaces2010 = cur.fetchall()

        cur.execute('SELECT White, AfricanAmerican, AmericanIndianAlaska, Asian, HawaiianOtherPacificIslander, HispanicLatino, TwoOrMoreRaces, White+AfricanAmerican+AmericanIndianAlaska+Asian+HawaiianOtherPacificIslander+HispanicLatino+TwoOrMoreRaces FROM censustotal2020')
        totalRaces2020 = cur.fetchall()

        # White Percentage of the US Population 2000-2020
        totalPopulation2000 = totalRaces2000[0][7]
        totalWhite2000 = White2000[0][0]
        whitePercentage2000 = totalWhite2000 / totalPopulation2000 

        totalPopulation2010 = totalRaces2010[0][7]
        totalWhite2010 = White2010[0][0]
        whitePercentage2010 = totalWhite2010 / totalPopulation2010

        totalPopulation2020 = totalRaces2020[0][7]
        totalWhite2020 = White2020[0][0]
        whitePercentage2020 = totalWhite2020 / totalPopulation2020

        # African American Percentage of the US Population 2000-2020
        totalPopulation2000 = totalRaces2000[0][7]
        totalAfricanAmerican2000 = AfricanAmerican2000[0][0]
        africanamericanPercentage2000 = totalAfricanAmerican2000 / totalPopulation2000 

        totalPopulation2010 = totalRaces2010[0][7]
        totalAfricanAmerican2010 = AfricanAmerican2010[0][0]
        africanamericanPercentage2010 = totalAfricanAmerican2010 / totalPopulation2010

        totalPopulation2020 = totalRaces2020[0][7]
        totalAfricanAmerican2020 = AfricanAmerican2020[0][0]
        africanamericanPercentage2020 = totalAfricanAmerican2020 / totalPopulation2020

        # AmericanIndianAlaska Percentage of the US Population 2000-2020
        totalPopulation2000 = totalRaces2000[0][7]
        totalAmericanIndianAlaska2000 = AmericanIndianAlaska2000[0][0]
        AmericanIndianAlaskaPercentage2000 = totalAmericanIndianAlaska2000 / totalPopulation2000 

        totalPopulation2010 = totalRaces2010[0][7]
        totalAmericanIndianAlaska2010 = AmericanIndianAlaska2010[0][0]
        AmericanIndianAlaskaPercentage2010 = totalAmericanIndianAlaska2010 / totalPopulation2010

        totalPopulation2020 = totalRaces2020[0][7]
        totalAmericanIndianAlaska2020 = AmericanIndianAlaska2020[0][0]
        AmericanIndianAlaskaPercentage2020 = totalAmericanIndianAlaska2020 / totalPopulation2020

        # Asian Percentage of the US Population 2000-2020
        totalPopulation2000 = totalRaces2000[0][7]
        totalAsian2000 = Asian2000[0][0]
        AsianPercentage2000 = totalAsian2000 / totalPopulation2000 

        totalPopulation2010 = totalRaces2010[0][7]
        totalAsian2010 = Asian2010[0][0]
        AsianPercentage2010 = totalAsian2010 / totalPopulation2010

        totalPopulation2020 = totalRaces2020[0][7]
        totalAsian2020 = Asian2020[0][0]
        AsianPercentage2020 = totalAsian2020 / totalPopulation2020

        # HawaiianOtherPacificIslander Percentage of the US Population 2000-2020
        totalPopulation2000 = totalRaces2000[0][7]
        totalHawaiianOtherPacificIslander2000 = HawaiianOtherPacificIslander2000[0][0]
        HawaiianOtherPacificIslanderPercentage2000 = totalHawaiianOtherPacificIslander2000 / totalPopulation2000 

        totalPopulation2010 = totalRaces2010[0][7]
        totalHawaiianOtherPacificIslander2010 = HawaiianOtherPacificIslander2010[0][0]
        HawaiianOtherPacificIslanderPercentage2010 = totalHawaiianOtherPacificIslander2010 / totalPopulation2010

        totalPopulation2020 = totalRaces2020[0][7]
        totalHawaiianOtherPacificIslander2020 = HawaiianOtherPacificIslander2020[0][0]
        HawaiianOtherPacificIslanderPercentage2020 = totalHawaiianOtherPacificIslander2020 / totalPopulation2020

        # HispanicLatino Percentage of the US Population 2000-2020
        totalPopulation2000 = totalRaces2000[0][7]
        totalHispanicLatino2000 = HispanicLatino2000[0][0]
        HispanicLatinoPercentage2000 = totalHispanicLatino2000 / totalPopulation2000 

        totalPopulation2010 = totalRaces2010[0][7]
        totalHispanicLatino2010 = HispanicLatino2010[0][0]
        HispanicLatinoPercentage2010 = totalHispanicLatino2010 / totalPopulation2010

        totalPopulation2020 = totalRaces2020[0][7]
        totalHispanicLatino2020 = HispanicLatino2020[0][0]
        HispanicLatinoPercentage2020 = totalHispanicLatino2020 / totalPopulation2020

        # TwoOrMoreRaces Percentage of the US Population 2000-2020
        totalPopulation2000 = totalRaces2000[0][7]
        totalTwoOrMoreRaces2000 = TwoOrMoreRaces2000[0][0]
        TwoOrMoreRacesPercentage2000 = totalTwoOrMoreRaces2000 / totalPopulation2000 

        totalPopulation2010 = totalRaces2010[0][7]
        totalTwoOrMoreRaces2010 = TwoOrMoreRaces2010[0][0]
        TwoOrMoreRacesPercentage2010 = totalTwoOrMoreRaces2010 / totalPopulation2010

        totalPopulation2020 = totalRaces2020[0][7]
        totalTwoOrMoreRaces2020 = TwoOrMoreRaces2020[0][0]
        TwoOrMoreRacesPercentage2020 = totalTwoOrMoreRaces2020 / totalPopulation2020

if __name__ == "__main__":
    main()