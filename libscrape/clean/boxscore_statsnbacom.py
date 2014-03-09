import re
import datetime
import time
import json
import logging

from libscrape.config import config
from libscrape.config import db
from libscrape.config import constants 
import player


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT
LOGDIR_SOURCE = constants.LOGDIR_SOURCE


class Clean:

    def __init__(self, filename, gamedata, dbobj):
        self.raw_data = open(LOGDIR_EXTRACT + filename,'r').read()
        self.dbobj = dbobj
        self.game = gamedata
        self.filename = filename
        self.PlayerResolve = player.Resolve(self.dbobj)


    def clean(self):
        data = json.loads(self.raw_data)
        self.parseTeamData(data)
        self.parseGameStats(data)
        self.parsePlayers(data)
        #self.parseOfficials(data)


    def parsePlayers(self, raw):
        data = []
        for line in raw['resultSets']:
            if line['name'] in ['PlayerStats']:
                header = line['headers']
                for row in line['rowSet']:
                    newdata = dict(zip([a.lower() for a in header], row))
                    newdata = self._cleanGameIdKeys(newdata)
                    newdata = self._resolveTeam(newdata)
                    newdata = self._resolvePlayer(newdata)
                    data.append(newdata)

        data = self._convertKeys(data)
        data = self._resolveDeciseconds(data, 'deciseconds_played')

        self._dumpFile(data, self.filename)


    def parseTeamData(self, data):
        d = []

        for line in data['resultSets']:
            if line['name'] in ['TeamStats','LineScore']:
                header = line['headers']
                for row in line['rowSet']:
                    newdata = dict(zip([a.lower() for a in header], row))
                    newdata = self._cleanGameIdKeys(newdata)
                    newdata = self._resolveTeam(newdata)
                    d.append(newdata)

            if line['name'] in ['OtherStats']:
                header = line['headers']
                for row in line['rowSet']:
                    newdata = dict(zip([a.lower() for a in header], row))
                    newdata = self._cleanGameIdKeys(newdata)
                    newdata = self._resolveTeam(newdata)
                    d.append(newdata)

        d = self._removeKeys(d)
        d = self._convertKeys(d)
        d = self._resolveDeciseconds(d, 'deciseconds_elapsed')
                
        self._dumpFile(d, self.filename + '_game_stats_team')


    def parseGameStats(self, raw):
        data = []
        for line in raw['resultSets']:
            if line['name'] in ['GameInfo']:
                header = line['headers']
                for row in line['rowSet']:
                    newdata = dict(zip([a.lower() for a in header], row))
                    newdata['duration'] = newdata['game_time']
                    newdata['game_id'] = self.game['id']

                    del newdata['game_time']
                    del newdata['game_date']

                    data.append(newdata)

        self._dumpFile(data, self.filename + '_game_stats')


    def parseOfficials(self, data):
        for line in data['resultSets']:
            if line['name'] == 'Officials':
                header = line['headers']
                for row in line['rowSet']:
                    print dict(zip([a.lower() for a in header], row))


    def _cleanGameIdKeys(self, data):
        d = data.copy()
        if 'game_id' in d.keys():
            d['statsnbacom_game_id'] = d['game_id']

        d['game_id'] = self.game['id']

        return d


    def _resolveTeam(self, data):
        away_team = self.dbobj.query_dict("SELECT * FROM team WHERE id = %s" % (self.game['away_team_id']))[0]
        home_team = self.dbobj.query_dict("SELECT * FROM team WHERE id = %s" % (self.game['home_team_id']))[0]

        d = data.copy()
        d['statsnbacom_team_id'] = d['team_id']
        d['statsnbacom_team_abbreviation'] = d['team_abbreviation']
        del d['team_abbreviation']

        if 'team_city_name' in d.keys():
            d['statsnbacom_team_city'] = d['team_city_name']
            del d['team_city_name']
        if 'team_city' in d.keys():
            d['statsnbacom_team_city'] = d['team_city']
            del d['team_city']
        if 'team_name' in d.keys():
            d['statsnbacom_team_name'] = d['team_name']
            del d['team_name']

        if away_team['nbacom_code'] == data['team_abbreviation'] or away_team['statsnbacom_team_id'] == data['team_id']:
            d['team_id'] = away_team['id']
        elif home_team['nbacom_code'] == data['team_abbreviation'] or home_team['statsnbacom_team_id'] == data['team_id']:
            d['team_id'] = home_team['id']
        else:
            d['team_id'] = 0

        return d


    def _removeKeys(self, data):
        newdata = []
        remove_keys = [
            'game_date_est',
            'league_id',
        ]

        for line in data:
            for rk in remove_keys:
                if rk in line.keys():
                    del line[rk]

            newdata.append(line)

        return newdata


    def _convertKeys(self, data):
        newdata = []
        key_conversion = {
            'pts': 'points',
            'reb': 'rebounds',
            'ast': 'assists',
            'blk': 'blocks',
            'stl': 'steals',
            'to': 'turnovers',
            'pf': 'fouls',
            'oreb': 'rebounds_offensive',
            'dreb': 'rebounds_defensive',
            'fg3m': 'threeptm',
            'fg3a': 'threepta',
            'fg3_pct': 'threeptfg',
            'fg_pct': 'fg',
            'ft_pct': 'ft',
            'pts_2nd_chance': 'points_second_chance',
            'pts_paint': 'points_in_paint',
            'pts_fb': 'points_fb',
            'season_id': 'statsnbacom_season_id',
        }

        for line in data:
            for key, value in key_conversion.items():
                if key in line.keys():
                    line[value] = line[key]
                    del line[key]

            newdata.append(line)

        return newdata


    def _resolveDeciseconds(self, data, key_name):
        newdata = []
        for line in data:
            line[key_name] = 0

            if 'min' in line.keys(): 
                if line['min'] is not None:
                    minutes, seconds = line['min'].split(':')
                    line[key_name] = (int(minutes) * 60 + int(seconds)) * 10

                del line['min']

            newdata.append(line)

        return newdata


    def _resolvePlayer(self, data):
        newdata = data.copy()
        newdata['statsnbacom_player_id'] = newdata['player_id']
        newdata['statsnbacom_player_name'] = newdata['player_name']
        del newdata['player_id']
        del newdata['player_name']

        player_id = self.PlayerResolve.matchByStatsNbaComId(newdata['statsnbacom_player_id'])
        if not player_id:
            player_id = -1
            logging.info("BOXSCORE_STATSNBACOM - game_id: %s - Did not find match by statsnbacom_player_id: %s" % (self.game['id'], newdata['statsnbacom_player_id']))
            # Need a resolve by player name here

        newdata['player_id'] = player_id

        return newdata



    def _dumpFile(self, data, filename):
        f = open(LOGDIR_CLEAN + filename,'w')
        data_json = json.dumps(data)
        f.write(data_json)


def main():

    dbobj = db.Db(config.dbconn_prod_nba)

    game = dbobj.query_dict("SELECT * FROM game WHERE id = %s" % (4766))[0]
    filename = '%s_boxscore_statsnbacom' % (game['abbrev'])
    obj = Clean(filename, game, dbobj)
    obj.clean()


if __name__ == '__main__':
    main()
