import csv
import os
import datetime
import json
import logging

import find_player
from libscrape.config import db
from libscrape.config import constants 
from libscrape.config import config



LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class Clean:

    def __init__(self, filename, game, dbobj):
        self.raw_data = open(LOGDIR_EXTRACT + filename,'r').read()
        self.filename = filename
        self.game = game
        self.dbobj = dbobj


    def clean(self):
        shots = self._parse()
        shots = self._resolveShotCoordinates(shots)
        shots = self._resolveDecisecondsLeft(shots)
        shots = self._resolveTeam(shots)
        shots = self._resolvePlayers(shots)
        shots = self._addGameId(shots)
        shots = self._deleteFields(shots)
        self._dumpFile(shots)


    def _parse(self):
        shots = []
        data = json.loads(self.raw_data)
        for line in data['resultSets']:
            if 'name' in line.keys() and line['name'] == 'Shot_Chart_Detail':

                for event in line['rowSet']:
                    shots.append(dict(zip([header.lower() for header in line['headers']],event)))

        return shots


    def _resolveShotCoordinates(self, shots): 
        data = []
        for shot in shots:
            shot['x'] = shot['loc_x']
            shot['y'] = shot['loc_y'] + 50 # y = 0 is the location of the rim, not the baseline

            data.append(shot)

        return data


    def _deleteFields(self, shots):
        data = []
        for shot in shots:
            del shot['loc_x']
            del shot['loc_y']
            del shot['shot_zone_basic']
            del shot['shot_zone_range']
            del shot['shot_zone_area']
            del shot['grid_type']
            del shot['minutes_remaining']
            del shot['seconds_remaining']
            del shot['team_name']
            data.append(shot)

        return data


    def _resolveDecisecondsLeft(self, shots):
        data = []
        for shot in shots:
            shot['deciseconds_left'] = (shot['minutes_remaining'] * 60 +  shot['seconds_remaining']) * 10
            data.append(shot)

        return data


    def _resolveTeam(self, shots):
        data = []
        away_team_name = self.dbobj.query_dict("SELECT name FROM team WHERE id = %s" % (self.game['away_team_id']))[0]['name']
        home_team_name = self.dbobj.query_dict("SELECT name FROM team WHERE id = %s" % (self.game['home_team_id']))[0]['name']

        for shot in shots:
            shot['statsnbacom_team_id'] = shot['team_id']
            shot['statsnbacom_team_name'] = shot['team_name']
            shot['team_id'] = 0
            if shot['team_name'] == away_team_name:
                shot['team_id'] = self.game['away_team_id']
            elif shot['team_name'] == home_team_name:
                shot['team_id'] = self.game['home_team_id']

            data.append(shot)

        return data


    def _resolvePlayers(self, shots):
        fpobj = find_player.FindPlayer(self.dbobj)
        home_players = fpobj._transformPlayersToTuples(self._getPlayers(self.game['home_team_id']))
        away_players = fpobj._transformPlayersToTuples(self._getPlayers(self.game['away_team_id']))

        data = []
        for shot in shots:
            if shot['team_id'] == self.game['home_team_id']:
                player_list = home_players
            elif shot['team_id'] == self.game['away_team_id']:
                player_list = away_players
            else:
                player_list = []

            shot['player_id'] = fpobj.matchPlayerByNameApproximate(shot['player_name'], player_list)
            data.append(shot)

        return data


    def _getPlayers(self, team_id):
        return self.dbobj.query_dict("""
            SELECT pnba.player_id, pnba.team_id, pnba.last_name, p.full_name, p.full_name_alt1, p.full_name_alt2 
            FROM player_nbacom_by_game pnba 
                INNER JOIN player p ON p.id = pnba.player_id 
            WHERE pnba.game_id = %s AND pnba.team_id = %s
        """ % (self.game['id'], team_id))


    def _addGameId(self, shots):
        data = []
        for shot in shots:
            shot['game_id'] = self.game['id']
            data.append(shot)

        return data


    def _dumpFile(self, shots):
        f = open(LOGDIR_CLEAN + self.filename,'w')
        shot_json = json.dumps(shots)
        f.write(shot_json)


def main():

    dbobj = db.Db(config.dbconn_prod_nba)
    files = [f for f in os.listdir('../../dump/extract') if 'shotchart_statsnbacom' in f]
    f = '2013-11-26_LAL@WAS_shotchart_statsnbacom'
    gamedata = dbobj.query_dict("SELECT * FROM game WHERE id = 4356")[0]

    obj = Clean(f, gamedata, dbobj)
    obj.clean()



if __name__ == '__main__':
    main()
