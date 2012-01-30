import re
import datetime
import csv
from BeautifulSoup import BeautifulStoneSoup
import os
import json


from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class CleanBoxScore:

    def __init__(self, filename, gamedata, dbobj):
        self.xml = open(LOGDIR_EXTRACT + filename,'r').read()
        self.soup = BeautifulStoneSoup(self.xml)
        self.gamedata = gamedata
        self.filename = filename
        self.db = dbobj


    def clean(self):
        player_stats = self.getStats()
        player_stats = self._addGameId(player_stats)

        self._dumpFile(player_stats)


    def getOfficials(self):
        soupofficials = self.soup.find("officials")
        
        officials = dict(soupofficials.attrs)['nm'].split('|')
        print officials


    def getPlayerLines(self):
        team_data = self.soup.find("vtm")
        players = team_data.findAll("pl")

        for p in players:
            print p.attrs
        

    def getTeamNames(self):
        soup = self.soup
        home_team = soup.find("htm")
        away_team = soup.find("vtm")
       
        print home_team['tm']
        print away_team['tm']


    def getStats(self):
        soup = self.soup
        playbyplaydata = soup.findAll("pl")

        home_team = soup.find("htm")
        away_team = soup.find("vtm")
        existing_players = self._getExistingPlayerIds()

        player_stats = []
        for team_name, team in [('home',home_team), ('away',away_team)]:
            players = team.findAll("pl")

            for p in players:
                player_stat_line = {}
                player_data = p['name'].split('|')
                nbacom_player_id = player_data[0]

                try:
                    player_stat_line['player_id'] = existing_players[nbacom_player_id]
                except:
                    player_stat_line['player_id'] = 0

                parsed_stats = self._parseStatLine(p['stat'])
                player_stat_line.update(parsed_stats)
                
                # Check if the player was a DNP
                if p['dnp'] == 'DNP':
                    player_stat_line['is_dnp'] = 1
                else:
                    player_stat_line['is_dnp'] = 0

                player_stats.append(player_stat_line)

        return player_stats

        
    def _parseStatLine(self,raw_stats):
        # unknown13 is blank
        # I think unknown12 is PER, but have to confirm later

        # Pre-populate a dictionary of zero values
        data = {}
        keys = ('time_played','fg','threept','ft','off_reb','def_reb','total_reb','assists','pfouls','steals','turnovers','blocks','unknown12','unknown13','total_points','plusminus','blocks_against') 
        for k in keys:
            data.setdefault(k,0)
   
        # Update default dictionary if the value isn't a blank string 
        statdata = dict(zip(keys,raw_stats.split('|')))
        for key, val in statdata.items():
            if val != '' and val != ':':
                data[key] = val

        # Convert time to seconds
        if data['time_played'] and data['time_played'] != ':':
            data['sec_played'] = int(data['time_played'].split(':')[0]) * 60 + int(data['time_played'].split(':')[1])
        else:
            data['sec_played'] = 0

        # Split field goals in to made/attempted
        if data['fg']:
            data['fgm'] = data['fg'].split('-')[0]
            data['fga'] = data['fg'].split('-')[1]
            del data['fg']
        else:
            data['fgm'] = 0
            data['fga'] = 0
        
        # Split free throws in to made/attempted
        if data['ft']:
            data['ftm'] = data['ft'].split('-')[0]
            data['fta'] = data['ft'].split('-')[1]
            del data['ft']
        else:
            data['ftm'] = 0
            data['fta'] = 0
        
        # Split three pointers in to made/attempted
        if data['threept']:
            data['threeptm'] = data['threept'].split('-')[0]
            data['threepta'] = data['threept'].split('-')[1]
            del data['threept']
        else:
            data['threeptm'] = 0
            data['threepta'] = 0

        return data
        

    def _getExistingPlayerIds(self):
        players = self.db.query_dict("SELECT * FROM player_resolved_test")
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['nbacom_player_id']] = player['id']

        return players_indexed


    def _addGameId(self, player_data):
        player_data_adjusted = []
       
        
        for line in player_data:
            
            line['game_id'] = self.gamedata['id'] 
            player_data_adjusted.append(line)

        return player_data_adjusted


    def _dumpFile(self, data):
        f = open(LOGDIR_CLEAN + self.filename,'w')
        data_json = json.dumps(data)
        f.write(data_json)


def main():

    files = [f for f in os.listdir(LOGDIR_EXTRACT) if '2011-12' in f and 'boxscore' in f]
    f = '2012-01-18_OKC@WAS_boxscore_nbacom'

    gamedata = db.nba_query_dict("SELECT * FROM game where date_played = '2012-01-18'") 

    for g in gamedata:
        print g['abbrev']
        f = g['abbrev'] + '_boxscore_nbacom'

        obj = CleanBoxScore(f, g)
        obj.clean()
    

if __name__ == '__main__':
    main()
