import sqlite3
from plot import *
import plotly.graph_objs as go
from scrape import *
from builddatabase import *
def plot_pattern1(result):
    print("Plotting...")
    tid=[x[0] for x in result]
    tname=[x[1] for x in result]
    tcountry=[x[2] for x in result]
    trace=[x[3] for x in result]
    tteam=[x[4] for x in result]
    tearn=[x[5] for x in result]
    tall=[x[6] for x in result]
    tp=[x[7] for x in result]
    tt=[x[8] for x in result]
    tz=[x[9] for x in result]
    fig = go.Figure(data=[go.Table(header=dict(values=['Id', 'Name','Country','Race','Team','Total Earning','vsALL','vsP','vsT','vsZ']),
                 cells=dict(values=[tid, tname,tcountry,trace,tteam,tearn,tall,tp,tt,tz]))])
    fig.update_layout(title="The Searching Result according to the Query Options")
    fig.show()
def plot_bar(result,kind,race):
    print("Plotting...")
    type=kind[3:]
    tid=[x[0] for x in result]
    text=[x[1] for x in result]
    twin=[]
    for t in text:
        if t=='Unknown':
            t='0'
        twin.append(t)
    fig = go.Figure(data=[go.Bar(
            x=tid, y=twin,
            text=text,
            textposition='auto',
        )])
    fig.update_layout(title=race+type)
    fig.show()
def plot_pattern2(result):
    print("Plotting...")
    tname=[x[0] for x in result]
    tseries=[x[1] for x in result]
    tprize=[x[2] for x in result]
    tlocation=[x[3] for x in result]
    twinner=[x[4] for x in result]
    trunnerup=[x[5] for x in result]
    tplayer=[x[6] for x in result]
    fig = go.Figure(data=[go.Table(header=dict(values=['Name', 'Series','Prize','Location','Winner','RunnerUp','Players']),
                 cells=dict(values=[tname, tseries,tprize,tlocation,twinner,trunnerup,tplayer]))])
    fig.update_layout(title="The information of premier tournaments in 2019")
    fig.show()
def plot_pie(result,country,team):
    print("Plotting...")
    if len(country)==0:
        country='all around the world'
    if len(team)==0:
        team='all teams'
    tid=[x[0] for x in result]
    tname=[x[1] for x in result]
    fig = go.Figure(data=[go.Pie(labels=tid, values=tname, hole=.3)])
    fig.update_layout(title="Distribution of players'game race of"+team+' in '+country)
    fig.show()
def process_command(command,Test=False):
    result=[]
    if command.split(',')[0].lower() == 'player':
        result=command_player(command,Test)
    if command.split(',')[0].lower() == 'team':
        result=command_team(command,Test)
    if command.split(',')[0].lower() == 'race':
        result=command_race(command,Test)
    if command.split(',')[0].lower() == 'winrate':
        result=command_winrate(command,Test)
    if command.split(',')[0].lower() == 'premier':
        result=command_premier(command,Test)
    return result
def command_player(command,Test=False):
    parameter_list=command.split(',')
    Id=''
    reverse='DESC'
    kind='p1.[Total Earnings]'
    limit='10'
    race=''
    while True:
        result=[]
        for command in parameter_list[1:]:
            if command[0:3]=='id=':
                Id='WHERE p1.[Game id]="'+command[3:]+'" '
            elif command[0:5]=='name=':
                Id='WHERE p1.Name="'+command[5:]+'" '
            elif command[0:8]=='country=':
                Id='WHERE c1.EnglishName="'+command[8:]+'" '
            elif command[0:7]=='region=':
                Id='WHERE c1.Region="'+command[7:]+'" '
            elif command[0:5]=='race=':
                race='AND p1.[Race in Game]="'+command[5:]+'" '
            elif command=='Earning':
                kind='p1.[Total Earnings]'
            elif command=='vALL':
                kind='p1.vsALL'
            elif command=='vP':
                kind='p1.vsP'
            elif command=='vT':
                kind='p1.vsT'
            elif command=='vZ':
                kind='p1.vsZ'
            elif command[0:4]=='top=':
                reverse='DESC'
                limit=command[4:]
                if limit.isdigit() is False:
                    result.append(('Command not recognized: Input integer as limit',))
                    return result
            elif command[0:7]=='bottom=':
                reverse=''
                limit=command[7:]
                if limit.isdigit() is False:
                    result.append(('Command not recognized: Input integer as limit',))
                    return result
            else:
                result.append(('Command not recognized:'+command,))
                return result
        conn = sqlite3.connect('SC2.db')
        cur = conn.cursor()
        statement = '''SELECT p1.[Game id], p1.Name, c1.EnglishName, p1.[Race in Game], p1.team, p1.[Total Earnings],p1.vsALL,p1.vsP,p1.vsT,P1.vsZ
                    FROM Players as p1 JOIN Countries as c1 ON p1.Country=c1.Id
                    {}
                    {}
                    GROUP BY p1.[Game id]
                    ORDER BY {}
                    {} LIMIT {}
                  '''.format(Id,race,kind,reverse,limit)
        cur.execute(statement)
        for row in cur:
            result1 = []
            for r in row:
                result1.append(r)
            result.append(result1)
            result[-1][5] = '$' + str(int(result[-1][5]))
            try:
                result[-1][6] = str(int(result[-1][6])) + '%'
            except:
                result[-1][6]='Unknown'
            try:
                result[-1][7] = str(int(result[-1][7])) + '%'
            except:
                result[-1][7]='Unknown'
            try:
                result[-1][8] = str(int(result[-1][8])) + '%'
            except:
                result[-1][8]='Unknown'
            try:
                result[-1][9] = str(int(result[-1][9])) + '%'
            except:
                result[-1][9]='Unknown'
        conn.commit()
        conn.close()
        if len(result)!=0:
            if Test==False:
                plot_pattern1(result)
        return result
def command_team(command,Test=False):
    parameter_list=command.split(',')
    Name='WHERE p1.Team="KaiZi Gaming"'
    reverse='DESC'
    kind='p1.[Total Earnings]'
    limit='10'
    race=''
    while True:
        result=[]
        for command in parameter_list[1:]:
            if command[0:5]=='team=':
                Name='WHERE p1.Team="'+command[5:]+'" '
            elif command[0:5]=='race=':
                race='AND p1.[Race in Game]="'+command[5:]+'" '
            elif command=='Earning':
                kind='p1.[Total Earnings]'
            elif command=='vALL':
                kind='p1.vsALL'
            elif command=='vP':
                kind='p1.vsP'
            elif command=='vT':
                kind='p1.vsT'
            elif command=='vZ':
                kind='p1.vsZ'
            elif command[0:4]=='top=':
                reverse='DESC'
                limit=command[4:]
                if limit.isdigit() is False:
                    result.append(('Command not recognized: Input integer as limit',))
                    return result
            elif command[0:7]=='bottom=':
                reverse=''
                limit=command[7:]
                if limit.isdigit() is False:
                    result.append(('Command not recognized: Input integer as limit',))
                    return result
            else:
                result.append(('Command not recognized:'+command,))
                return result
        conn = sqlite3.connect('SC2.db')
        cur = conn.cursor()
        statement = '''SELECT p1.[Game id], p1.Name, c1.EnglishName, p1.[Race in Game], p1.team, p1.[Total Earnings],p1.vsALL,p1.vsP,p1.vsT,P1.vsZ
                    FROM Players as p1 JOIN Countries as c1 ON p1.Country=c1.Id
                    {}
                    {}
                    GROUP BY p1.[Game id]
                    ORDER BY {}
                    {} LIMIT {}
                  '''.format(Name,race,kind,reverse,limit)
        cur.execute(statement)
        for row in cur:
            result1 = []
            for r in row:
                result1.append(r)
            result.append(result1)
            result[-1][5] = '$' + str(int(result[-1][5]))
            try:
                result[-1][6] = str(int(result[-1][6])) + '%'
            except:
                result[-1][6]='Unknown'
            try:
                result[-1][7] = str(int(result[-1][7])) + '%'
            except:
                result[-1][7]='Unknown'
            try:
                result[-1][8] = str(int(result[-1][8])) + '%'
            except:
                result[-1][8]='Unknown'
            try:
                result[-1][9] = str(int(result[-1][9])) + '%'
            except:
                result[-1][9]='Unknown'
        conn.commit()
        conn.close()
        if len(result)!=0:
            if Test==False:
                plot_pattern1(result)
        return result
def command_winrate(command,Test=False):
    parameter_list=command.split(',')
    while True:
        result=[]
        race='Zerg'
        kind='p1.vsALL'
        limit='10'
        reverse='DESC'
        for command in parameter_list[1:]:
            if command[0:5]=='race=':
                race=command[5:]
            elif command=='vALL':
                kind='p1.vsALL'
            elif command=='vP':
                kind='p1.vsP'
            elif command=='vT':
                kind='p1.vsT'
            elif command=='vZ':
                kind='p1.vsZ'
            elif command[0:4]=='top=':
                reverse='DESC'
                limit=command[4:]
                if limit.isdigit() is False:
                    result.append(('Command not recognized: Input integer as limit',))
                    return result
            elif command[0:7]=='bottom=':
                reverse=''
                limit=command[7:]
                if limit.isdigit() is False:
                    result.append(('Command not recognized: Input integer as limit',))
                    return result
            else:
                result.append(('Command not recognized:'+command,))
                return result
        conn = sqlite3.connect('SC2.db')
        cur = conn.cursor()
        statement = '''SELECT p1.[Game id],{}
                    FROM Players as p1 JOIN Countries as c1 ON p1.Country=c1.Id
                    WHERE p1.[Race in Game]="{}"
                    GROUP BY p1.[Game id]
                    ORDER BY {}
                    {} LIMIT {}
                  '''.format(kind,race,kind,reverse,limit)
        cur.execute(statement)
        for row in cur:
            result1 = []
            for r in row:
                result1.append(r)
            result.append(result1)
            try:
                result[-1][1] = str(int(result[-1][1])) + '%'
            except:
                result[-1][1]='Unknown'
        conn.commit()
        conn.close()
        if len(result)!=0:
            if Test==False:
                plot_bar(result,kind,race)
        return result
def command_premier(command,Test=False):
    parameter_list=command.split(',')
    while True:
        result=[]
        series=''
        kind='p.Prize'
        winrace=''
        for command in parameter_list[1:]:
            if command[0:7]=='series=':
                series='WHERE p.Series="'+command[7:]+'" '
            elif command[0:5]=='name=':
                series='WHERE p.Name="'+command[5:]+'" '
            elif command=='prize':
                kind='p.Prize'
            elif command=='players':
                kind='p.Players'
            elif command[0:11]=='winnerrace=':
                winrace='AND p1.[Race in Game]="'+command[11:]+'" '
            else:
                result.append(('Command not recognized:'+command,))
                return result
        conn = sqlite3.connect('SC2.db')
        cur = conn.cursor()
        statement = '''SELECT p.Name, p.Series, p.Prize, p.Location,p1.[Game id],p2.[Game id],p.Players
                    FROM Premiers as p JOIN Players as p1 ON p.Winner=p1.Id
                    JOIN Players as p2 ON p.RunnerUp=p2.Id
                    {}
                    {}
                    ORDER BY {} DESC
                  '''.format(series,winrace,kind)
        cur.execute(statement)
        for row in cur:
            result1 = []
            for r in row:
                result1.append(r)
            result.append(result1)
            result[-1][2] = '$' + str(int(result[-1][2]))
        conn.commit()
        conn.close()
        if len(result)!=0:
            if Test==False:
                plot_pattern2(result)
        return result
def command_race(command,Test=False):
    parameter_list=command.split(',')
    while True:
        result=[]
        country=''
        team=''
        c=''
        t=''
        for command in parameter_list[1:]:
            if command[0:8]=='country=':
                country='WHERE c1.EnglishName="'+command[8:]+'"'
                c=command[8:]
            elif command[0:7]=='region=':
                country='WHERE c1.Region="'+command[7:]+'"'
                c=command[7:]
            elif command[0:5]=='team=':
                team='AND p1.Team="'+command[5:]+'" '
                t=command[5:]
            else:
                result.append(('Command not recognized:'+command,))
                return result
        conn = sqlite3.connect('SC2.db')
        cur = conn.cursor()
        statement = '''SELECT p1.[Race in Game],count(*)
                    FROM Players as p1
                    JOIN Countries as c1 on p1.Country=c1.id
                    {}
                    {}
                    GROUP BY p1.[Race in Game]
                  '''.format(country,team)
        cur.execute(statement)
        for row in cur:
            result1 = []
            for r in row:
                result1.append(r)
            result.append(result1)
        conn.commit()
        conn.close()
        if len(result)!=0:
            if Test==False:
                plot_pie(result,c,t)
        return result
def load_help_text():
    with open('help.txt') as f:
        return f.read()

def interactive_prompt():
    help_text = load_help_text()
    response = ''
    command_list=['help','exit','player','team','race','winrate','premier','map']
    print('''Welcome to the StarCraftII information query system. Thank you for being
intereted in StarCraftII.Please input the query command below.If it is the
first time you use the system or just need some help you could input "help"
to get the using manual of this system. Thank you very much!
        ''')
    while response != 'exit':
        response = input('Please,enter a command and split options with "," or input "help" to get user manual: ')
        if len(response)==0:
            result=[('',)]
        elif response.split(',')[0].lower() in command_list:
            if response.split(',')[0].lower() == 'help':
                if len(response.split(','))>1:
                    print('Command not recognized: '+response)
                else:
                    print(help_text)
                continue
            elif response.split(',')[0].lower() =='map':
                if len(response.split(','))>1:
                    print('Command not recognized: '+response)
                else:
                    print("Plotting...")
                    plot_premier()
                continue
            elif response.split(',')[0].lower() =='exit':
                if len(response.split(','))>1:
                    print('Command not recognized: '+response)
                else:
                    print("Program end")
                continue
            else:
                result=process_command(response)
                if len(result)==0:
                    print("There is no result matching your query options! Please Try another query.")
                else:
                    for r in result:
                        c = ''
                        for n in r:
                            if 'Command' in str(n):
                                c+=str(n)
                                print(c)
                continue
        else:
            print('Command not recognized: '+response)


if __name__=="__main__":
    print("Initialization...might need 20 minutes if you choose do not using cache")
    get_players_from_liquidpedia()
    get_premier_from_liquidpedia()
    build_database()
    interactive_prompt()
