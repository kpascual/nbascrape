import csv
import json

from libscrape.config import db
from libscrape.config import constants 
import libscrape.config.constants



LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class CleanShots:
    def __init__(self, filename, gamedata, dbobj):
        self.filename = filename
        self.gamedata = gamedata
        self.away_team = self.gamedata['away_team_id']
        self.home_team = self.gamedata['home_team_id']
        self.game_name = self.gamedata['abbrev']
        self.game_id = self.gamedata['id']
        self.date_played = self.gamedata['date_played']
        self.db = dbobj

        self.players = [line for line in csv.reader(open(LOGDIR_EXTRACT + self.filename + '_players','r'),delimiter=',',lineterminator='\n')]
        self.shots = self._getShots()


    def clean(self):

        cleaned = []
        cleaned1 = self.adjustFourthPeriod(self.shots)
        cleaned2 = self.adjustTeam(cleaned1)
        cleaned3 = self.adjustXYCoordinates(cleaned2)
        cleaned4 = self.resolvePlayerId(cleaned3)
        cleaned5 = self.addGameId(cleaned4)
        
        self._dumpIntoFile(cleaned5)

    
    def _dumpIntoFile(self, shots):
        f = open(LOGDIR_CLEAN + self.filename,'wb')
        f.write(json.dumps(shots))


    def _getShots(self):
        filename = LOGDIR_EXTRACT + self.filename + '_shots'
        data = [line for line in csv.reader(open(filename,'r'),delimiter=',',lineterminator='\n')]
        headers = ['shot_num','team_code','time_left','period','cbssports_player_id','shot_type_cbssports_id','is_shot_made','x','y','distance']

        all_data = []
        for line in data:
            final_data = dict(zip(headers,line))
            all_data.append(final_data)

        return all_data
 

    def adjustFourthPeriod(self, data):

        cleaned = []
        last_period = 1
        current_period = 1
        last_seconds = 7201
        for counter, line in enumerate(data):

            new_time = line['time_left'].split(':')
            if len(new_time) == 2:
                new_seconds = int(int(new_time[0])*60 + int(new_time[1])) * 10
                line['deciseconds_left'] = int(int(new_time[0])*60 + int(new_time[1])) * 10
            else:
                line['deciseconds_left'] = int(float(line['time_left']) * 10)

            if last_seconds < new_seconds and new_seconds - last_seconds > 1500:
                if int(last_period) >= 3:
                    current_period = current_period + 1
                else:
                    current_period = int(line['period'])

            line['period'] = current_period 

            last_period = current_period
            last_seconds = new_seconds

            del line['time_left']
           
            cleaned.append(line) 

        return cleaned


    def adjustXYCoordinates(self, shots):
        cleaned = []
        for line in shots:
            line['x'] = int(line['x']) * 10

            if line['team_id'] == self.away_team:
                line['y'] = (47 - int(line['y'])) * 10
            else:
                line['y'] = (47 + int(line['y'])) * 10

            cleaned.append(line)

        return cleaned


    def adjustTeam(self, data):
        # Team: 0 = Away Team, 1 = Home team
        cleaned = []
        for line in data:
            if int(line['team_code']) == 0:
                line['team_id'] = self.away_team
            else:
                line['team_id'] = self.home_team
            
            del line['team_code']
            
            cleaned.append(line)

        return cleaned


    def resolvePlayerId(self, data):
        players = self._getPlayerIdsInGame()
        
        cleaned = []
        for line in data:
            
            try:
                line['player_id'] = players[int(line['cbssports_player_id'])]
            except:
                line['player_id'] = 0
            
            del line['cbssports_player_id']
            cleaned.append(line)

        return cleaned 


    def _getPlayerIdsInGame(self):
        players = self.db.query_dict("SELECT * FROM player")
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['cbssports_player_id']] = player['id']

        return players_indexed

         
    def addGameId(self, data):
        cleaned = []
        for line in data:
            line['game_id'] = self.game_id
            cleaned.append(line)

        return cleaned


def run(game, filename, dbobj):
    shotvars = {
        'filename':  filename,
        'gamedata':  game,
        'dbobj'   :  dbobj
    }
    CleanShots(**shotvars).clean()

