from BeautifulSoup import BeautifulStoneSoup
import csv
import os
import logging
import datetime
import re
import difflib
import json
from libscrape.config import db
from libscrape.config import constants 



LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class Clean:

    def __init__(self, filename, gamedata, dbobj):
        self.xml = open(LOGDIR_EXTRACT + filename,'r').read()
        self.filename = filename
        self.soup = BeautifulStoneSoup(self.xml)
        self.date_played = filename.replace(LOGDIR_EXTRACT,'')[:10]
        self.gamedata = gamedata
        self.db = dbobj


    def cleanAll(self):
        raw_shots = self.soup.findAll('shot')
        shots = [dict(shot.attrs) for shot in raw_shots]
        
        shots_adjusted = self.resolveShotCoordinates(shots)
        shots_adjusted = self.resolvePlayerIds(shots_adjusted)
        shots_adjusted = self.resolveTeam(shots_adjusted)
        shots_adjusted = self.resolveMadeMissed(shots_adjusted)
        shots_adjusted = self.parseShotDescription(shots_adjusted)
        shots_adjusted = self.addGameId(shots_adjusted)
        shots_adjusted = self.resolveGameTime(shots_adjusted)

        self._dumpFile(shots_adjusted)


    def parseData(self):
        shots = self.soup.findAll('shot')

        home_x = []
        home_y = []
        away_x = []
        away_y = []
        for shot in shots:
            data = dict(shot.attrs)
            if data['t'] == 'h':
                home_x.append(int(data['x']))
                home_y.append(int(data['y']))
            else:
                away_x.append(int(data['x']))
                away_y.append(int(data['y']))

        return (away_x, home_x)


    def resolveShotCoordinates(self, shots):

        # x-coordinates are the width of the floor (50 feet) 0-50
        # y-coordinates are the length of the court (94 feet) 0-94
        adjusted_shots = []
        for shot in shots:

            if shot['t'] == 'h':
                # Convert y-coordinate to feet from baseline 0.
                # y-coordinate shows feet away from coordinate 94 ft.
                # Then multiply by 10 (coordinates stored in feet times 10)
                shot['y'] = (94 - int(shot['y'])) * 10

                # Convert x-coordinate to -250 to 250
                # x = 0 is the middle of the court (location of basket), and +/- 250 are the sidelines 
                shot['x'] = (int(shot['x']) * 10) - 250
            else:
                # Away team's coordinates start at 0 and go upward.  No transformation necessary
                shot['y'] = int(shot['y']) * 10
                shot['x'] = (int(shot['x']) * 10) - 250
               
            adjusted_shots.append(shot)

        return adjusted_shots 

    
    def resolvePlayerIds(self, shots):
        players = self._getPlayerIds()
        player_names = [name for player_id, name in sorted(players.items())]
        player_ids = [player_id for player_id, name in sorted(players.items())]

        shots_adjusted = []
        for shot in shots:
            
            player_name = shot['p']

            match = difflib.get_close_matches(player_name,player_names,1, 0.8)
            
            if match:
                shot['player_id'] = player_ids[player_names.index(match[0])]
            else:
                shot['player_id'] = 0

            shots_adjusted.append(shot)

        return shots_adjusted


    def resolveTeam(self, shots):
        shots_adjusted = []
        for shot in shots:
            if shot['t'] == 'h':
                shot['t'] = self.gamedata['home_team_id']
            elif shot['t'] == 'a':
                shot['t'] = self.gamedata['away_team_id']
                
            shots_adjusted.append(shot)

        return shots_adjusted


    def resolveMadeMissed(self, shots):
        # made=true/false
        shots_adjusted = []
        for shot in shots:
            if shot['made'] == 'true':
                shot['result'] = 1
            elif shot['made'] == 'false':
                shot['result'] = 0
               
            shots_adjusted.append(shot)

        return shots_adjusted


    def parseShotDescription(self, shots):
        shots_adjusted = []
        for shot in shots:
            match = re.search('(Made|Miss)\s+(?P<distance>[0-9]{1,2})ft\s+(?P<shot_type>[0-9a-zA-Z\-\s]+)\s+(?P<min>[0-9]{1,2}):(?P<sec>[0-9]{2}).*',shot['d'])

            if match:
                shot = dict(shot.items() + match.groupdict().items())

            shots_adjusted.append(shot)

        return shots_adjusted


    def addGameId(self, shots):
        shots_adjusted = []
        for shot in shots:
            shot['game_id'] = self.gamedata['id'] 
            shots_adjusted.append(shot)

        return shots_adjusted


    def resolveGameTime(self, shots):
        shots_adjusted = []
        for shot in shots:
            # Keep time in deciseconds.
            shot['time_left'] = (int(shot['min']) * 60 + int(shot['sec'])) * 10
            shots_adjusted.append(shot)

        return shots_adjusted


    def _getPlayerIds(self):
        players = self.db.query_dict("""
            SELECT p.*
            FROM player p
                INNER JOIN player_nbacom_by_game g ON g.nbacom_player_id = p.nbacom_player_id
            WHERE g.game_id = %s
        """ % (self.gamedata['id']))
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['id']] = player['first_name'] + " " + player['last_name']

        return players_indexed


    def _dumpFile(self, shots):
        f = open(LOGDIR_CLEAN + self.filename,'w')
        shot_json = json.dumps(shots)
        f.write(shot_json)

def main():

    files = [
        '2011-12-25_LAC@GS_shotchart_espn',
        '2011-12-25_MIA@DAL_shotchart_espn',
        '2011-12-25_BOS@NY_shotchart_espn',
        '2011-12-25_CHI@LAL_shotchart_espn',
        '2011-12-25_ORL@OKC_shotchart_espn'
    ]

    files = [f for f in os.listdir('../../logs/extract') if 'shotchart_espn' in f]

    f = '2011-12-25_LAC@GS_shotchart_espn'
    gamedata = db.nba_query_dict("SELECT * FROM game WHERE id = 1267")[0]
    obj = ShotChartEspn(f, gamedata)
    obj.cleanAll()



if __name__ == '__main__':
    main()
