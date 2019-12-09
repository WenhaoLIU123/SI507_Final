import sqlite3
import json
DBNAME = 'SC2.db'
PLAYERSJSON='player.json'
COUNTRIESJSON = 'countries.json'
PREMIERJSON='premier.json'
def build_database():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'DROP TABLE IF EXISTS "Players";'
    cur.execute(statement)
    statement = 'DROP TABLE IF EXISTS "Countries";'
    cur.execute(statement)
    statement = 'DROP TABLE IF EXISTS "Premiers";'
    cur.execute(statement)
    statement = '''
                CREATE TABLE 'Players' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'Game id' TEXT,
                    'Name' TEXT,
                    'Country' TEXT,
                    'Race in Game' TEXT,
                    'Team' TEXT,
                    'Total Earnings' REAL,
                    'vsALL' REAL,
                    'vsP' REAL,
                    'vsT' REAL,
                    'vsZ' REAL
                );
            '''
    try:
        cur.execute(statement)
    except:
        pass
    player_file = open('player.json', 'r', encoding='utf-8')
    player_contents = player_file.read()
    PLAYER_DICTION = json.loads(player_contents)
    player_file.close()
    for players in PLAYER_DICTION:
        Gid=players['id']
        try:
            Name=players['Name:']
        except:
            Name='Unknown'
        Country=players['Country:'].strip()
        Race=players['Race:']
        try:
            Team=players['Team:']
        except:
            Team='Not assigned in any team'
        Earn=players['Total Earnings:'].replace('$','')
        Earn=Earn.replace(',','')
        try:
             vsa=players['vsALL'].split('%')[0]
        except:
            vsa='NULL'
        try:
             vsp=players['vsP'].split('%')[0]
        except:
            vsp='NULL'
        try:
             vst=players['vsT'].split('%')[0]
        except:
            vst='NULL'
        try:
             vsz=players['vsZ'].split('%')[0]
        except:
            vsz='NULL'
        statement='''INSERT INTO Players VALUES (NULL,"{}","{}","{}","{}","{}",{},{},{},{},{})'''.format(Gid,Name,Country,Race,Team,Earn,vsa,vsp,vst,vsz)
        cur.execute(statement)

    statement = '''
                CREATE TABLE 'Countries' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'Alpha2' TEXT,
                    'Alpha3' TEXT,
                    'EnglishName' TEXT,
                    'Region' TEXT,
                    'Subregion' TEXT,
                    'Population' INTEGER,
                    'Area' REAL
                );
            '''
    try:
        cur.execute(statement)
    except:
        pass
    country_file = open('countries.json', 'r', encoding='utf-8')
    country_contents = country_file.read()
    COUNTRY_DICTION = json.loads(country_contents)
    country_file.close()
    for country in COUNTRY_DICTION:
        a2=country['alpha2Code']
        a3=country['alpha3Code']
        EN=country['name']
        Region=country['region']
        SubR=country['subregion']
        Pop=country['population']
        if country['area'] is None:
            Area='NULL'
        else:
             Area=country['area']
        statement='''INSERT INTO Countries VALUES (NULL,'{}','{}',"{}","{}","{}",{},{})'''.format(a2,a3,EN,Region,SubR,Pop,Area)
        cur.execute(statement)
    statement = '''
                CREATE TABLE 'Premiers' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'StartDate' TEXT,
                    'EndDate' TEXT,
                    'Name' TEXT,
                    'Series' TEXT,
                    'Prize' REAL,
                    'Players' INTEGER,
                    'Location' TEXT,
                    'Winner' TEXT,
                    'RunnerUp' TEXT,
                    'Lat' FLOAT,
                    'Lng' FLOAT
                );
            '''
    try:
        cur.execute(statement)
    except:
        pass
    premier_file = open('premier.json', 'r', encoding='utf-8')
    premier_contents = premier_file.read()
    PREMIER_DICTION = json.loads(premier_contents)
    premier_file.close()
    for premiers in PREMIER_DICTION:
        start=premiers['start'].split()[0]
        end=premiers['end'].split()[0]
        Name=premiers['name']
        Series=premiers['series']
        location=premiers['location']
        prize=premiers['prize'].replace('$','')
        prize=prize.replace(',','')
        playern=premiers['players']
        winner=premiers['winner']
        run=premiers['runner-up']
        lat=premiers['lat']
        lng=premiers['lng']
        statement='''INSERT INTO Premiers VALUES (NULL,"{}","{}","{}","{}",{},{},"{}","{}","{}",{},{})'''.format(start,end,Name,Series,prize,playern,location,winner,run,lat,lng)
        cur.execute(statement)

    statement='''UPDATE Players
                        SET Country=(SELECT Id from Countries WHERE Players.Country=Countries.EnglishName)
                     '''
    cur.execute(statement)
    statement='''UPDATE Premiers
                        SET Winner=(SELECT Id from Players WHERE Premiers.Winner=Players.[Game id])
                     '''
    cur.execute(statement)
    statement='''UPDATE Premiers
                        SET RunnerUp=(SELECT Id from Players WHERE Premiers.RunnerUp=Players.[Game id])
                     '''
    cur.execute(statement)
    conn.commit()
    conn.close()
