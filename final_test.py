from builddatabase import *
from query import *
from plot import *
from scrape import *
import unittest
header = {'User-agent': 'Mozilla/5.0'}
DENAME='SC2.db'
class Test_access(unittest.TestCase):
    def testplayeraccess(self):
        url='https://liquipedia.net/starcraft2/Players_(All)'
        resp = requests.get(url, headers=header).text
        resp=BeautifulSoup(resp,'html.parser')
        list=resp.find_all(class_='sortable wikitable')
        self.assertGreaterEqual(len(list),65)
    def testplayerinfoaccess(self):
        url='https://liquipedia.net/starcraft2/Serral'
        resp = requests.get(url, headers=header).text
        resp=BeautifulSoup(resp,'html.parser')
        list=resp.find(class_='fo-nttax-infobox wiki-bordercolor-light')
        id=list.find(class_='infobox-header').text
        id=id.replace('[e][h] ','')
        self.assertEqual(id,'Serral')
    def testwinrateaccess(self):
        url='http://aligulac.com/players/485/'
        resp = requests.get(url, headers=header).text
        resp=BeautifulSoup(resp,'html.parser')
        list=resp.find(class_='tab-content')
        all=list.find(class_='text-right').text
        all=all.strip()
        self.assertEqual(all,'All')
    def testpremier(self):
        url='https://liquipedia.net/starcraft2/Premier_Tournaments'
        resp = requests.get(url, headers=header).text
        resp=BeautifulSoup(resp,'html.parser')
        list=resp.find_all(class_='sortable wikitable smwtable jquery-tablesorter')
        Premier=list[1]
        all=Premier.find_all('td')
        self.assertEqual(all[0].text.strip(),'2019-11-21  Nov 21')


class Test_json(unittest.TestCase):
    def testPlayer_json(self):
        player_file = open('player.json', 'r', encoding='utf-8')
        player_contents = player_file.read()
        PLAYER_DICTION = json.loads(player_contents)
        player_file.close()
        player1=PLAYER_DICTION[11]
        self.assertEqual(player1['id'],'goblin')
        self.assertEqual(player1['Race:'],'Protoss')
        self.assertEqual(player1['vsP'],'61.09% (303/496)')
        player2=PLAYER_DICTION[156]
        self.assertEqual(player2['id'],'EGG')
        self.assertEqual(player2['Race:'],'Zerg')
        self.assertRaises(KeyError, player2.get('vsALL'))
    def testPremier_json(self):
        premier_file = open('premier.json', 'r', encoding='utf-8')
        premier_contents = premier_file.read()
        PREMIER_DICTION = json.loads(premier_contents)
        premier_file.close()
        premier1=PREMIER_DICTION[1]
        self.assertEqual(premier1['name'],'2019 WCS Global Finals')
        self.assertEqual(premier1['lat'],33.8365932)
        self.assertEqual(premier1['runner-up'],'Reynor')
        premier2=PREMIER_DICTION[7]
        self.assertEqual(premier2['series'],'GSL')
        self.assertEqual(premier2['location'],'Seoul')
        self.assertEqual(premier2['winner'],'Rogue')
        self.assertEqual(premier2['prize'],'$141,856')
class TestDatabase(unittest.TestCase):

    def test_player_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT [Game id] FROM Players'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('INnoVation',), result_list)
        self.assertEqual(len(result_list), 401)

        sql = '''
            SELECT [Game id], Team, [Race in Game],
                   [Total Earnings]
            FROM Players
            WHERE Country=211
            ORDER BY vsALL DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 52)
        self.assertEqual(result_list[0][2], 'Zerg')

        conn.close()

    def test_country_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT EnglishName
            FROM Countries
            WHERE Region="Oceania"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('New Zealand',), result_list)
        self.assertEqual(len(result_list), 27)

        sql = '''
            SELECT COUNT(*)
            FROM Countries
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertTrue(count == 250 or count == 251)

        conn.close()
    def test_premier_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Series FROM Premiers'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('GSL',), result_list)
        self.assertEqual(len(result_list), 17)

        sql = '''
            SELECT Name, Prize, Winner,Location
            FROM Premiers
            WHERE Series="WCS"
            ORDER BY Prize DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 7)
        self.assertEqual(result_list[0][3], 'Anaheim')

        conn.close()
    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Alpha2
            FROM Players
                JOIN Countries
                ON Players.Country=Countries.Id
            WHERE Team="Not assigned in any team"
                AND [Race in Game]="Zerg"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('KR',), result_list)
        sql = '''
            SELECT Series
            FROM Players
                JOIN Premiers
                ON Players.ID=Premiers.Winner
            WHERE [Game id]="Serral"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('HSC',), result_list)
        conn.close()
class TestPlayerSearch(unittest.TestCase):

    def test_player_search(self):
        results = process_command('player,id=Maru',Test=True)
        self.assertEqual(results[0][3], 'Terran')

        results = process_command('player,name=Alex Sunderhaft,vT',Test=True)
        self.assertEqual(results[0][4], 'Not assigned in any team')

        results = process_command('player,country=Korea (Republic of),race=Zerg,vALL,top=10',Test=True)
        self.assertEqual(results[3][0], 'Rogue')
        self.assertEqual(results[5][5],'$256685')

        results = process_command('player,region=Europe,Earning,bottom=5',Test=True)
        self.assertEqual(results[0][4], 'Escuela Española Sc2')
        self.assertEqual(results[3][2], 'Czech Republic')

        try:
            plot_pattern1(results)
        except:
            self.fail()


class TestTeamSearch(unittest.TestCase):

    def test_team_search(self):
        results = process_command('team,team=TSGaming,race=Protoss,vT',Test=True)
        self.assertEqual(results[1][0], 'Nice')

        results = process_command('team,team=Not assigned in any team,Earning,top=10',Test=True)
        self.assertEqual(results[1][0], 'Stats')

        try:
            plot_pattern1(results)
        except:
            self.fail()

class TestWinSearch(unittest.TestCase):

    def test_winrate_search(self):
        results = process_command('winrate,race=Terran,vZ,top=5',Test=True)
        self.assertEqual(results[1][0],'INnoVation')
        self.assertEqual(results[2][1],'66%')

        results = process_command('winrate,race=Protoss,vALL,bottom=10',Test=True)
        self.assertEqual(results[3][0],'Sakura')
        self.assertEqual(results[9][1],'40%')
        kind='p1.vsALL'
        race='Protoss'
        try:
            plot_bar(results,kind,race)
        except:
            self.fail()


class TestRaceSearch(unittest.TestCase):

    def test_race_search(self):
        results = process_command('race,region=Europe',Test=True)
        self.assertEqual(results[0][1], 50)
        self.assertEqual(results[1][0], 'Random')
        self.assertEqual(len(results), 4)

        results = process_command('race,country=Korea (Republic of),team=Jin Air Green Wings',Test=True)
        self.assertEqual(results[0][1], 3)
        self.assertEqual(results[1][0], 'Terran')
        self.assertEqual(len(results), 3)
        country='Korea (Republic of)'
        team='Jin Air Green Wings'
        try:
            plot_pie(results,country,team)
        except:
            self.fail()
class TestPremierSearch(unittest.TestCase):

    def test_premier_search(self):
        results = process_command('premier,series=WCS,prize',Test=True)
        self.assertEqual(results[0][2], "$700000")
        self.assertEqual(results[1][4], 'Serral')
        self.assertEqual(len(results), 7)

        results2 = process_command('premier,name=2019 Global StarCraft II League Season 3,winnerrace=Zerg',Test=True)
        self.assertEqual(results2[0][3], "Seoul")
        self.assertEqual(results2[0][1], 'GSL')
        self.assertEqual(len(results2), 1)
        try:
            plot_pattern2(results)
        except:
            self.fail()
class TestMapping(unittest.TestCase):

    def testConstructor(self):
        P=premier(location='Seoul',name='2019 GSL vs the World',series='WCS',prize='82743',winner='Serral',runnerup='Elazer',lat=0,lng=0)
        self.assertEqual(P.location,'Seoul')
        self.assertEqual(P.runnerup,'Elazer')
        self.assertEqual(P.lng,0)
        self.assertEqual(str(P),'Name: 2019 GSL vs the World Series: WCS Prize: $82743 Winner: Serral RunnerUp: Elazer<br>')
    def test_map(self):
        try:
            plot_premier()
        except:
            self.fail()
if __name__ == "__main__":
    unittest.main(verbosity=2)