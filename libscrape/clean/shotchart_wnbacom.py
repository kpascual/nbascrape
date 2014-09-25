from BeautifulSoup import BeautifulStoneSoup
import csv
import os
import datetime
import json
import logging
from libscrape.config import db
from libscrape.config import constants 
from libscrape.config import config



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

        self.home_team = self.gamedata['home_team_id']
        self.away_team = self.gamedata['away_team_id']


    def cleanAll(self):
        shots = self.getShots()

        shots_adjusted = self.resolveShotCoordinates(shots)
        shots_adjusted = self.resolvePlayerIds(shots_adjusted)
        shots_adjusted = self.resolveTeam(shots_adjusted)
        shots_adjusted = self.resolveMadeMissed(shots_adjusted)
        shots_adjusted = self.addGameId(shots_adjusted)

        self._dumpFile(shots_adjusted)
        logging.info("CLEAN - shotchart_nbacom - game_id: %s - shot count: %s" % (self.gamedata['id'], len(shots_adjusted)))

    def getShots(self):
        raw_shots = self.soup.findAll('event')
        return [dict(shot.attrs) for shot in raw_shots]

    def resolvePlayerIds(self, shots):
        players = self._getPlayerIds()

        shots_adjusted = []
        for shot in shots:
            nbacom_player_id = shot['pid'].split('|')[0]

            try:
                shot['player_id'] = players[nbacom_player_id]
            except:
                shot['player_id'] = 0
                logging.warning("CLEAN - shotchart_nbacom - game_id: %s - cant match player: '%s'" % (self.gamedata['id'],shot['pid']))

            shots_adjusted.append(shot)

        return shots_adjusted
            

    def _getPlayerIds(self):
        players = self.db.query_dict("SELECT * FROM player")
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['nbacom_player_id']] = player['id']

        return players_indexed


    def resolveShotCoordinates(self, shots):
        # NBA.com's coordinates are 840 for the length of the court (94 ft) 
        # and 250 for the width of the court (50 ft)
        
        # The 840 total pixels for length of the court refers to the distance between the two hoops (84 ft)
        # (4 ft from baseline to each backboard, and an 18-inch diameter rim, 9 inch radius)
        # For away teams, it appears the x-coordinate is flipped 
        new_shots = [] 
        for shot in shots:
            newshot = shot.copy()

            # X coordinate is the width of the court
            # Y coordinate is the length
            newshot['y'] = int(shot['y']) + 50
            new_shots.append(newshot)

        return new_shots

    
    def resolveGameTime(self):
        # NBA.com shot chart data is already broken up by period and tenths of a second.
        # Transformation not necessary
        pass


    def resolveTeam(self, shots):
        shots_adjusted = []
        for shot in shots:
            if shot['tm'] == 'h':
                shot['tm'] = self.home_team
            elif shot['tm'] == 'v':
                shot['tm'] = self.away_team
                
            shots_adjusted.append(shot)

        return shots_adjusted


    def resolveMadeMissed(self, shots):
        # 1 = Made; 2 = Missed
        shots_adjusted = []
        for shot in shots:
            if shot['typ'] == '1':
                shot['result'] = 1
            elif shot['typ'] == '2':
                shot['result'] = 0
            else:
                shot['result'] = -1
               
            del shot['typ'] 
            shots_adjusted.append(shot)

        return shots_adjusted
    

    def addGameId(self, shots):
        shots_adjusted = []
        for shot in shots:
            shot['game_id'] = self.gamedata['id'] 
            shots_adjusted.append(shot)

        return shots_adjusted


    def _dumpFile(self, shots):
        f = open(LOGDIR_CLEAN + self.filename,'w')
        shot_json = json.dumps(shots)
        f.write(shot_json)


class CleanWnba(Clean):
    def resolveShotCoordinates(self, shots):
        new_shots = [] 
        for shot in shots:
            newshot = shot.copy()

            # For women, the x-coordinate is actually the length of the floor, and the y-coordinate the width of the floor
            # For vorped purposes, we need to flip them

            newshot['x'] = shot['y']
            newshot['y'] = int(shot['x']) + 50
            
            new_shots.append(newshot)

        return new_shots


def run(game, filename, dbobj):
    CleanWnba(filename, game, dbobj).cleanAll()


def main():

    dbobj = db.Db(db.dbconn_prod)
    files = [f for f in os.listdir('../../dump/extract') if 'shotchart_nbacom' in f]
    f = '2013-06-20_SA@MIA_shotchart_nbacom'
    gamedata = dbobj.query_dict("SELECT * FROM game WHERE id = 4043")[0]

    obj = CleanWnba(f, gamedata, dbobj)
    shots = obj.getShots()
    print obj.resolveShotCoordinates(shots)



if __name__ == '__main__':
    main()
