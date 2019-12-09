import requests
import json
from bs4 import BeautifulSoup
import plotly
import plotly.graph_objs as go
from secrets import google_places_key


CACHE_FNAME = 'cache.json'
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

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print('from cache')
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        if API is True:
        # Make the request and cache the new data
            resp = requests.get(url).json()
            CACHE_DICTION[unique_ident] = resp
            dumped_json_cache = json.dumps(CACHE_DICTION,indent=4)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close() # Close the open file
            return CACHE_DICTION[unique_ident]
        # Make the request and cache the new data
        resp = requests.get(url, headers=header).text
        if content is None:
            CACHE_DICTION[unique_ident] = resp
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close() # Close the open file
        else:
            page_soup=BeautifulSoup(resp,'html.parser')
            # print(page_soup)
            content=page_soup.find(class_=content)
            # print(content)
            content=str(content)
            CACHE_DICTION[unique_ident]=content
            dumped_json_cache=json.dumps(CACHE_DICTION)
            fw=open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close()

        return CACHE_DICTION[unique_ident]

def get_players_from_liquidpedia():
    # some of sites of al do not have street address
    result=[]
    base_url='https://liquipedia.net/starcraft2/Players_(All)'
    header = {'User-agent': 'Mozilla/5.0'}
    content='mw-parser-output'
    LIST=make_request_using_cache(base_url,header,content)
    LIST=BeautifulSoup(LIST,'html.parser')
    list=LIST.find_all(class_='sortable wikitable')
    count=0
    information=[]
    for l in list:
        list_td=l.find_all('td')
        for i in range(len(list_td)):
            if i>1:
                if i%6==0:#401
                    player={}
                    url=list_td[i].find('a')['href']
                    next_url='https://liquipedia.net'
                    next_url+=url
                    content='fo-nttax-infobox wiki-bordercolor-light'
                    count+=1
                    info=make_request_using_cache(next_url,header,content)
                    info=BeautifulSoup(info,'html.parser')
                    detail=info.find_all(class_='infobox-cell-2')
                    id=info.find(class_='infobox-header').text
                    id=id.replace('[e][h] ','')
                    player['id']=id
                    for i in range(len(detail)):
                        if i%2==0:
                            title=detail[i].text
                            if title=='Country:':
                                infom=detail[i+1].find_all('a')[1].text
                            else:
                                infom=detail[i+1].text
                            title=title.replace(u'\xa0', u' ')
                            infom=infom.replace(u'\xa0', u' ')
                            infom=infom.replace('Zerg, Protoss','Zerg')
                            infom=infom.replace("USA", 'United States of America')
                            infom=infom.replace("Russia", 'Russian Federation')
                            infom=infom.replace("South Korea", 'Korea (Republic of)')
                            infom=infom.replace("United Kingdom", 'United Kingdom of Great Britain and Northern Ireland')
                            infom=infom.replace("Bolivia", 'Bolivia (Plurinational State of)')
                            infom=infom.replace("Venezuela", 'Venezuela (Bolivarian Republic of)')
                            infom=infom.replace("Vietnam", 'Viet Nam')
                            if infom.strip()=='United States':
                                infom='United States of America'
                            # infom=infom.replace("United States", 'United States of America')
                            player[title]=infom.strip()
                    rate=info.find(class_='infobox-center infobox-icons')
                    links=rate.find_all('a')
                    for e in links:
                        link=e['href']
                        if 'aligulac.com/players/' in link:
                            winrateurl=link
                            content='tab-content'
                            LIST=make_request_using_cache(winrateurl,header,content)
                            LIST=BeautifulSoup(LIST,'html.parser')
                            allrate=LIST.find(class_='progress-bar progress-bar-default').text
                            allrate=allrate.strip()
                            player['vsALL']=allrate
                            vprate=LIST.find(class_='progress-bar progress-bar-success').text
                            vprate=vprate.strip()
                            player['vsP']=vprate
                            vtrate=LIST.find(class_='progress-bar progress-bar-primary').text
                            vtrate=vtrate.strip()
                            player['vsT']=vtrate
                            vzrate=LIST.find(class_='progress-bar progress-bar-danger').text
                            vzrate=vzrate.strip()
                            player['vsZ']=vzrate
                    information.append(player)
    filename='player.json'
    with open(filename,'w',encoding='utf-8') as f:
        json.dump(information,f,indent=4)
    return result
def get_premier_from_liquidpedia():
    result=[]
    base_url='https://liquipedia.net/starcraft2/Premier_Tournaments'
    header = {'User-agent': 'Mozilla/5.0'}
    # content='sortable wikitable smwtable jquery-tablesorter'
    LIST=make_request_using_cache(base_url,header)
    LIST=BeautifulSoup(LIST,'html.parser')
    title=LIST.find_all(class_='sortable wikitable smwtable jquery-tablesorter')
    Premier=title[1]
    info=Premier.find_all('td')
    count=0
    for i in range(len(info)):
        if count==0:
            game={}
            game['start']=info[i].text.strip()
            count+=1
        elif count==1:
            game['end']=info[i].text.strip()
            count+=1
        elif count==2:
            game['name']=info[i].text.strip()
            count+=1
        elif count==3:
            game['series']=info[i].text.strip()
            count+=1
        elif count==4:
            game['prize']=info[i].text.strip()
            count+=1
        elif count==5:
            game['players']=info[i].text.strip()
            count+=1
        elif count==6:
            a=info[i].text.strip()
            if 'Online/Offline' in a:
                a="Burbank"
            if 'Anaheim' in a:
                a="Anaheim"
            game['location']=a
            name=a
            url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+name+"&inputtype=textquery&fields=formatted_address,name,geometry&key="+google_places_key
            place=make_request_using_cache(url,API=True)
            lat=place['candidates'][0]["geometry"]["location"]["lat"]
            lng=place['candidates'][0]["geometry"]["location"]["lng"]
            game['lat']=lat
            game['lng']=lng
            count+=1
        elif count==7:
            game['winner']=info[i].text.strip()
            count+=1
        elif count==8:
            game['runner-up']=info[i].text.strip()
            count=0
            result.append(game)
    filename='premier.json'
    with open(filename,'w',encoding='utf-8') as f:
        json.dump(result,f,indent=4)
