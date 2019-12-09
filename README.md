# SI507_Final
Contains the code for final project of SI507: An StarCraftII Player information System

The purpose of this program is to collect the basic information of the active Starcraft II professional players around the world such as 
name, nation, age, race (in the game) and the major tournaments hold in 2019 including location, winner and prize. The program aims at 
people who are unfamiliar to Starcraft II but interested in the game and want to learn more about the players and the game and those people 
who are familiar with the game and want to check the status of the players such as win rate and ranking status and result of 
major tournaments in 2019. Starcraft II is the greatest real-time strategy games designed by Blizzard and recently the DeepMind group is 
designing an AI called ‘AlphaStar’ to play the game automatically just like “AlphaGo”. 
This program intend to make more people to know this great game.

1. The data sources used in this project are shown below:
    1. The list of all activate professional players around the world:
       url:https://liquipedia.net/starcraft2/Players_(All)
    2. The personal information of professional players:
       url(one of them):https://liquipedia.net/starcraft2/Reynor
    3. The record of the winning rate with different races(in the game):
       url(one of them):http://aligulac.com/players/5414/
    4. The list of all premier tournaments hold in 2019 with some informations:
       url:https://liquipedia.net/starcraft2/Premier_Tournaments
    5. The countries.json which is used in the project3
    6. The Google Place API:
       search manual: https://developers.google.com/places/web-service/search
       how to get a Google Places API: 
       https://www.dropbox.com/s/uhbhueweyc3eq06/Google%20Place%20API%20Instruction.docx?dl=0
2. Other informations needed in the report

   The project uses plotly to make table and graphs and the links to getting started info for plotly is:
   https://plot.ly/python/getting-started/
   https://plot.ly/python/scattermapbox/
3. Brief description of code structure

   Serveal functions are used in this project and some data structures are created for data processing. The code was devided into serval parts according to their different function.
   1. scrape.py
      This file contains the code that crawling data from 4 website data sources above. There are two 
      main functions used in here: get_players_from_liquidpedia() and get_premier_from_liguidpedia. 
      These two function scrape basic infomation of players and premiers and save them in two different 
      lists with each dictionary for each player and premier. During the crawling, the data were
      processed to have a united form such as change the name of country same as the countries.json, use 
      only the first nation or race in the game of some player.
      These two data structures will be saved in player.json and premier.json and used in the database 
      building part
   2. builiddatbase.py
      This file is used to load data from player.json, premier.json and contries.json and use these data 
      to build database with servel foreign key. "builid_database" function will load data from three 
      json files and build database. The name of the database is: "SC2.db" which has three tables:
      players: contain the id, name, race(in game), team, total earnings, vsALL, vsP, vsT, vsZ winrate
               of each active professional SC2 player.
      country: contain the infomation of each country.
      premiers: contain the name, series, location,prize,players joined, winner, runner-up. latitude and
               and longitude of each premier tournaments hold in 2019.
   3. query.py
      This file contains the main part of the code.It has three main parts.
      The first part is the user interactive function. Users could input operation command to make the 
      query and output corressponding table/graphs. Additionally, an user manual is added in this 
      function either.
      The second part is the query part which is the most important part of the whole system. This 
      function will load data and according to the different operation to run different data processing
      sub-functions (function start with "command_"). Each sub-functions will draw data from database
      and processing them and return a data structure (list). The return of result is saved for further
      data processing for those data structures.
      The most important function in the second part is interactive_prompt() and process_command().
      The third part is the plot part which contains series function(function start with "plot_").
      This part will receive the result from the second part and do further data processing which will 
      modify the order of the data appropriate for makeing plot with plotly function.
   4. plot.py
      This part contains the operaion of "show the map of distribution of premier tournaments hold in  
      2019" with a class named "premier" and a function named "plot_premier". The class will save the 
      infomation of premier tournaments save in the database and have a str function could show the 
      infomation fo the tournament and those classes will be saved in a list. The "plot_premier()" 
      function could load those data and use MAPBOX in plotly to show them on the map with infomation 
      when put clicker on it.
   5. final_test.py
      contain four basic test parts and each test part has at least one test case and each of test case 
      has at least assert function or fail test. 17 tests in total and more than 30 asserat conditions.
4. Brief user guide
   To start the function correctly, user should downloaded whole files and put them together and set a 
   secrets.py contains "google_palces_key" which is API key of Google Places API and "MAPBOX_TOKEN"  
   which is the mapbox key for plotly. The package used in the project is shown in the "requirements.txt".
   When all settle down, run "Query.py" to start the system. The system will ask user to input command 
   to continue. User could input "help" to check specific command list for the different kind of queries 
   or just input "player", "team", "winrate", "premier", "race" or "map" to check the result of default 
   value. 
 
        Remeber to split options with comma and here is the command list that used for further detailed query:

        help

            Description: Output the helper manual
        exit

            Description: Quit the program
        player

            Description: Lists the basic infomation of players, according the specified parameters.

            Options:
                * id=<Game id> [default: none]
                Description: Specifies a player'ID used in game to limit the
                             result. Only one player's infomation will return as result

                * name=<Name> [default: none]
                Description: Specifies a player'real to limit the
                result. Only one player's infomation will return as result

                * country=<Country> [default:none]
                Description: Specifies players' nation to limit the result

                * region=<Region> [default: none]
                Description: Specifies players' nation's region to limit the result

                REMINDER: If those four options above are used at the same time, only the last option will be input to
                the query system

                * race=<Race> [default:none]
                Description: Specifies players' race used in game to limit the result

                * Earning|vALL|vP|vT|vZ [default:Earning]
                Description: Specifies whether to sort by player's total earning, vsALL winrate,
                vsProtoss winrate, vsTerran winrate and vsZerg winrate to limit the result

                * top=<limit>|bottom=<limit> [default: top=10]
                Description: Specifies whether to list the top <limit> matches or the
                bottom <limit> matches.

        team

            Description: Lists the basic information of teams including the basic infomation of players
                         according the specified paramters.

            Options:
                * team=<team_name> [default: KaiZi Gaming]
                Description: Specifies a team name to limit the result

                * race=<Race> [default:none]
                Description: Specifies players' race used in game in the team to limit the result

                * Earning|vALL|vP|vT|vZ [default:Earning]
                Description: Specifies whether to sort by player's total earning, vsALL winrate,
                vsProtoss winrate, vsTerran winrate and vsZerg winrate in the team to limit the result

                * top=<limit>|bottom=<limit> [default: top=10]
                Description: Specifies whether to list the top <limit> matches or the
                bottom <limit> matches.

        winrate

            Description: Lists the winning rate of different players of all games played according the specified paramters.

            Options:
            
                * race=<Race> [default:none]
                Description: Specifies players' race used in game in the team to limit the result

                * Earning|vALL|vP|vT|vZ [default:Earning]
                Description: Specifies whether to sort by player's total earning, vsALL winrate,
                vsProtoss winrate, vsTerran winrate and vsZerg winrate in the team to limit the result

                * top=<limit>|bottom=<limit> [default: top=10]
                Description: Specifies whether to list the top <limit> matches or the
                bottom <limit> matches.


        premier

            Description: Lists infomation of premier tournaments hold in 2019 according to specified parameters.

            Options:
                * series=<name>|name=<name> [default: none]
                Description: Specifies the series that premier tournaments belond to or the specific name of the premier
                tournament to limit the reuslt. When name is specified only one result will be returned.

                * prize|players [default: prize]
                Description: Specifies whether to sort by the prize of the tournament or
                the number of players who attend the tournament

                * winnerrace=<race> [default:none]
                Description: Specifies the race of the winner of the tournamnet to limit the result

        race

            Description: Lists the distribution of the race used in the game according to specified parameters

            Options:
                * country=<name>|region=<region_name> [default: Korea (Republic of)]
                Description: Specifies one country's or region's race(in game) distribution to limit the reuslt. .

                * team=<team> [default: none]
                Description: Specifies one team's race(in game) distribution to limit the reuslt.
        map

            Description: Draw the distribution of the premier tournaments hold in 2019

