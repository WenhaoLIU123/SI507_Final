import sqlite3
import json
import plotly
import requests
import plotly.graph_objs as go
from secrets import *
class premier():
    def __init__(self, location='None',name='None',series='None',prize='None',winner='None',runnerup='None',lat=0,lng=0):
        self.location = location
        self.name = name
        self.series = series
        self.prize = prize
        self.winner = winner
        self.runnerup = runnerup
        self.lat=lat
        self.lng=lng
    def __str__(self):
        word='Name: '+self.name+' Series: '+self.series+' Prize: $'+str(self.prize)+' Winner: '+self.winner+' RunnerUp: '+self.runnerup+'<br>'
        return word


CACHE_FNAME = 'plot_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url, header=None,content=None,API=False):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        if API is True:
            resp = requests.get(url).json()
            CACHE_DICTION[unique_ident] = resp
            dumped_json_cache = json.dumps(CACHE_DICTION,indent=4)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close() # Close the open file
            return CACHE_DICTION[unique_ident]
        resp = requests.get(url, headers=header).text
        if content is None:
            CACHE_DICTION[unique_ident] = resp
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close() # Close the open file
        else:
            page_soup=BeautifulSoup(resp,'html.parser')
            content=page_soup.find(class_=content)
            content=str(content)
            CACHE_DICTION[unique_ident]=content
            dumped_json_cache=json.dumps(CACHE_DICTION)
            fw=open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close()

        return CACHE_DICTION[unique_ident]

def collect_premier():
    DBNAME = 'SC2.db'
    latt=[]
    lngg=[]
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement='''SELECT p1.Location, p1.Name,p1.Series,p1.Prize,p2.[Game id] as winner, p3.[Game id] as runnerup,p1.Lat,p1.Lng
                FROM Premiers as p1 JOIN Players as p2
                JOIN Players as p3
                WHERE p2.Id=p1.Winner and p3.Id=p1.RunnerUp
    '''
    cur.execute(statement)
    result=[]
    for row in cur:
        pre=premier(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        result.append(pre)
    conn.commit()
    conn.close()
    return result
def plot_premier():
    lat_vals = []
    lon_vals = []
    text_vals = []
    list=collect_premier()
    seoul=''
    count=0
    countb=0
    burbank=''
    countk=0
    kiev=''
    for game in list:
        # name=game.location
        if game.location=='Seoul':
            seoul+=str(game)
            count+=1
            if count==6:
                text_vals.append(seoul)
                lat_vals.append(game.lat)
                lon_vals.append(game.lng)
        elif game.location=='Burbank':
            burbank+=str(game)
            countb+=1
            if countb==2:
                text_vals.append(burbank)
                lat_vals.append(game.lat)
                lon_vals.append(game.lng)
        elif game.location=='Kiev':
            kiev+=str(game)
            countk+=1
            if countk==2:
                text_vals.append(kiev)
                lat_vals.append(game.lat)
                lon_vals.append(game.lng)
        else:
            text_vals.append(str(game))
            lat_vals.append(game.lat)
            lon_vals.append(game.lng)
    layout = dict(
        title = 'Location of Premier Tournaments Hold in 2019',
        autosize=True,
        showlegend = False,
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            bearing=0,
            center=dict(
                lat=lat_vals[7],
                lon=lon_vals[7]
                ),
            pitch=0,
            zoom=2,
          ),
        )

    fig = go.Figure(data=go.Scattermapbox(
            lon = lon_vals,
            lat = lat_vals,
            text = text_vals,
            mode = 'markers',
            marker_color = 'red',
            ))

    fig.update_layout(layout)
    fig.show()

