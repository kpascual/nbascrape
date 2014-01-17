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

        self._dumpFile(player_stats, self.filename)
        self.getGameInfo()


    def getGameInfo(self):
        data = {}
        data.update(self.getOfficials())
        data.update(self.getOtherGameData())
        data['game_id'] = self.gamedata['id']

        self._dumpFile(data, self.filename + '_game_stats')
        

    def getOfficials(self):
        soupofficials = self.soup.find("officials")
        
        officials = dict(soupofficials.attrs)['nm'].split('^')

        return dict(zip(['official1','official2','official3'],officials))
       

    def getOtherGameData(self):
        # Get game-level data
        gamedata = self.soup.find("game")
        dict_gamedata = dict(gamedata.attrs)
        data = {}

        data['arena'] = dict_gamedata['arn']
        data['attendance'] = data['arena'].split('|')[3]
        data['duration'] = dict_gamedata['dur']
        data['local_game_start'] = dict_gamedata['timloc']
        data['home_game_start'] = dict_gamedata['timh']
        data['away_game_start'] = dict_gamedata['timv']
        data['unknown_game_start'] = dict_gamedata['timet']
        data['national'] = dict_gamedata['nbrd'].replace('\'','').replace('\"','')

        home_data = self.soup.find("htm")
        dict_home = dict(home_data.attrs)

        data['home_tv'] = dict_home['brd'].split('|')[0].replace('\'','').replace('\"','')
        data['home_radio'] = dict_home['brd'].split('|')[1].replace('\'','').replace('\"','')
        data['home_quarter_score'] = dict_home['scr']
        data['home_score'] = data['home_quarter_score'].split('|')[-1]
        data['home_record'] = dict_home['rcd'].replace('/','-')
        data['home_record_conference'] = dict_home['std'].split('|')[0]
        data['home_record_division'] = dict_home['std'].split('|')[1]

        away_data = self.soup.find("vtm")
        dict_away = dict(away_data.attrs)

        data['away_tv'] = dict_away['brd'].split('|')[0].replace('\'','').replace('\"','')
        data['away_radio'] = dict_away['brd'].split('|')[1].replace('\'','').replace('\"','')
        data['away_quarter_score'] = dict_away['scr']
        data['away_score'] = data['away_quarter_score'].split('|')[-1]
        data['away_record'] = dict_away['rcd'].replace('/','-')
        data['away_record_conference'] = dict_away['std'].split('|')[0]
        data['away_record_division'] = dict_away['std'].split('|')[1]

        return data


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

                # Name split by pipe: nbacom_player_id, nbacom_player_code (i.e. dirk_nowitzki), name, status, position, jersey number
                player_data = p['name'].split('|')
                nbacom_player_id = player_data[0]

                try:
                    player_stat_line['player_id'] = existing_players[nbacom_player_id]
                except:
                    player_stat_line['player_id'] = 0

                parsed_stats = self._parseStatLine(p['stat'])
                player_stat_line.update(parsed_stats)
                
                # Add team id
                if team_name == 'home':
                    player_stat_line['team_id'] = self.gamedata['home_team_id']
                else:
                    player_stat_line['team_id'] = self.gamedata['away_team_id']
                
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
        else:
            data['fgm'] = 0
            data['fga'] = 0
        del data['fg']
        
        # Split free throws in to made/attempted
        if data['ft']:
            data['ftm'] = data['ft'].split('-')[0]
            data['fta'] = data['ft'].split('-')[1]
        else:
            data['ftm'] = 0
            data['fta'] = 0
        del data['ft']
        
        # Split three pointers in to made/attempted
        if data['threept']:
            data['threeptm'] = data['threept'].split('-')[0]
            data['threepta'] = data['threept'].split('-')[1]
        else:
            data['threeptm'] = 0
            data['threepta'] = 0
        del data['threept']

        return data
        

    def _getExistingPlayerIds(self):
        players = self.db.query_dict("SELECT * FROM player")
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


    def _dumpFile(self, data, filename):
        f = open(LOGDIR_CLEAN + filename,'w')
        data_json = json.dumps(data)
        f.write(data_json)


def main():

    files = [f for f in os.listdir(LOGDIR_EXTRACT) if '2011-12' in f and 'boxscore' in f]
    f = '2012-01-18_OKC@WAS_boxscore_nbacom'

    gamedata = db.nba_query_dict("SELECT * FROM game where date_played <= '2012-02-10'") 
    dbobj = db.Db(db.dbconn_nba)

    for game in gamedata:
        #print game['abbrev']
        filename = game['abbrev'] + '_boxscore_nbacom'

        obj = CleanBoxScore(filename, game, dbobj)
        result = obj.getGameInfo()
        

    
       
    

if __name__ == '__main__':
    main()
