import logging
import logging.config
import csv

from libscrape.config import db
from libscrape.config import constants 
import libscrape.config.constants


logging.config.fileConfig('logging.conf')
logger = logging.getLogger("clean")

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
        self.shots = [line for line in csv.reader(open(LOGDIR_EXTRACT + self.filename + '_shots','r'),delimiter=',',lineterminator='\n')]

        self.finalfields = ['shot_num','team_id','deciseconds_left','period','player_id',
                            'shot_type_id','is_shot_made','x','y','distance','game_id']

    def clean(self):

        cleaned = []
        cleaned1 = self.adjustFourthPeriod(self.shots)
        cleaned2 = self.adjustTeam(cleaned1)
        cleaned3 = self.adjustXYCoordinates(cleaned2)
        cleaned4 = self.resolvePlayerId(cleaned3)
        cleaned5 = self.addGameId(cleaned4)

        self._dumpIntoFile(cleaned5)

    
    def _dumpIntoFile(self, plays):
        
        writer = csv.writer(open(LOGDIR_CLEAN + self.filename,'wb'),delimiter=',',lineterminator='\n')
        writer.writerows([self.finalfields] + plays)
        

    def adjustFourthPeriod(self, data):

        cleaned = []
        last_period = 1
        current_period = 1
        last_seconds = 7201
        for counter, (i,team,time_left,period,player_id,shot_type,result,x,y,distance) in enumerate(data):

            new_time = time_left.split(':')
            if len(new_time) == 2:
                new_seconds = int(int(new_time[0])*60 + int(new_time[1])) * 10
            else:
                new_seconds = int(float(time_left) * 10)

            if last_seconds < new_seconds and new_seconds - last_seconds > 1500:
                if int(last_period) >= 3:
                    current_period = current_period + 1
                else:
                    current_period = int(period)
 
            last_period = current_period
            last_seconds = new_seconds
            

            cleaned.append((i,team,new_seconds,current_period,player_id,shot_type,result,x,y,distance))

        return cleaned


    def adjustXYCoordinates(self, plays):
        cleaned = []
        for (i,team,time_left,period,player_id,shot_type,result,x,y,distance) in plays:
            adjusted_x = int(x) * 10

            if team == self.away_team:
                adjusted_y = (47 - int(y)) * 10
            else:
                adjusted_y = (47 + int(y)) * 10

            cleaned.append((i,team,time_left,period,player_id,shot_type,result,adjusted_x,adjusted_y,distance))

        return cleaned
        
    def _getConformedTime(self):
        return self.db.query_dict("SELECT * FROM dim_times")


    def replaceWithConformedTime(self, plays):
        conformed_times = self._getConformedTime()
        cleaned = []
        for (i,team,time_left,period,player_id,shot_type,result,x,y,distance) in plays:
            print time_left
            mins, secs = time_left.split(':')

            new_time_left = (int(mins) * 60 + int(secs)) * 10
            """
            try:
                found = [itm['sec_elapsed_game'] for itm in conformed_times if itm['period'] == period and itm['sec_left_period'] == time_left][0]
                time_elapsed = found
            except:
                logger.warn("time not found! period: %s, time: %s, counter: %s" % (period,time_left,i))
                time_elapsed = -1
            """
            cleaned.append((i,team,new_time_left,period,player_id,shot_type,result,x,y,distance))

        return cleaned


    def adjustTeam(self, data):
        # Team: 0 = Away Team, 1 = Home team
        cleaned = []
        for i,team,time_left,period,player_id,shot_type,result,x,y,distance in data:
            if int(team) == 0:
                team = self.away_team
            else:
                team = self.home_team
            
            cleaned.append((i,team,time_left,period,player_id,shot_type,result,x,y,distance))

        return cleaned


    def resolvePlayerId(self, data):
        players = self._getPlayerIdsInGame()
        
        cleaned = []
        for i,team,time_left,period,cbssports_player_id,shot_type,result,x,y,distance in data:
            
            try:
                new_player_id = players[int(cbssports_player_id)]
            except:
                new_player_id = 0
            
            cleaned.append((i,team,time_left,period,new_player_id,shot_type,result,x,y,distance))

        return cleaned 


    def _getPlayerIdsInGame(self):
        players = self.db.query_dict("SELECT * FROM player_resolved_test")
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['cbssports_player_id']] = player['id']

        return players_indexed

         
    def addGameId(self, data):
        cleaned = []
        for tup in data:
            new = list(tup) + [self.game_id]
            cleaned.append(new)

        return cleaned


