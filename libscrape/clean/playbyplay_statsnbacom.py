import re
import datetime
import time
import json
import find_player
import logging

from libscrape.config import config
from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT
LOGDIR_SOURCE = constants.LOGDIR_SOURCE


class Clean:

    def __init__(self, filename, gamedata, dbobj):
        self.raw_data = open(LOGDIR_EXTRACT + filename,'r').read()
        self.dbobj = dbobj
        self.game = gamedata
        self.filename = filename


    def clean(self):
        plays = self._parse()
        plays = self._resolveTeam(plays)
        plays = self._resolveScore(plays)
        plays = self._resolveDescription(plays)
        plays = self._resolveDecisecondsLeft(plays)
        plays = self._renameFields(plays)
        plays = self._resolvePlays(plays)
        plays = self._addGameId(plays)
        plays = self._deleteFields(plays)
        #for play in plays:
        #    print play
        self._dumpFile(plays)


    def _parse(self):
        plays = []

        data = json.loads(self.raw_data)
        for line in data['resultSets']:
            if 'name' in line.keys() and line['name'] == 'PlayByPlay':
                for event in line['rowSet']:
                    plays.append(dict(zip([header.lower() for header in line['headers']],event)))

        return plays


    def _resolveTeam(self, plays):
        data = []
        for play in plays:
            if play['homedescription']:
                play['team_id'] = self.game['home_team_id']
            elif play['visitordescription']:
                play['team_id'] = self.game['away_team_id']
            else:
                play['team_id'] = 0

            data.append(play)

        return data


    def _resolveScore(self, plays):
        data = []
        home_score = 0
        away_score = 0
        for play in plays:
            if play['score']:
                play['home_score'], play['away_score'] = play['score'].split(' - ')
                home_score = play['home_score']
                away_score = play['away_score']
            else:
                play['home_score'] = home_score
                play['away_score'] = away_score

            data.append(play)

        return data


    def _addGameId(self, plays):
        data = []
        for play in plays:
            play['game_id'] = self.game['id']
            data.append(play)

        return data


    def _resolveDescription(self, plays):
        data = []
        for play in plays:
            if play['homedescription']:
                play['description'] = play['homedescription']
            elif play['visitordescription']:
                play['description'] = play['visitordescription']
            else:
                play['description'] = play['neutraldescription']

            data.append(play)

        return data


    def _resolveDecisecondsLeft(self, plays):
        data = []
        for play in plays:
            time_left = play['pctimestring'].split(':')        
            play['deciseconds_left'] = (int(time_left[0]) * 60 + int(time_left[1])) * 10
            data.append(play)

        return data


    def _renameFields(self, plays):
        data = []
        for play in plays:
            play['game_event_id'] = play['eventnum']
            data.append(play)

        return data


    def _resolvePlays(self, plays):
        data = []
        patterns = self.dbobj.query_dict("SELECT id, re FROM play_type_statsnbacom ORDER BY priority ASC")
        for play in plays:
            play['play_type_statsnbacom_id'] = 0
            
            for pattern in patterns:
                match = re.match(pattern['re'], play['description'])
                if match:
                    play['play_type_statsnbacom_id'] = pattern['id']
                    break

            #if play['play_type_statsnbacom_id'] == 0:
            #    print play['description']
            data.append(play)

        return data


    def _deleteFields(self, plays):
        data = []
        for play in plays:
            del play['eventnum']
            del play['score']
            del play['scoremargin']
            data.append(play)

        return data


    def _dumpFile(self, plays):
        f = open(LOGDIR_CLEAN + self.filename,'w')
        play_json = json.dumps(plays)
        f.write(play_json)


def main():

    dbobj = db.Db(config.dbconn_prod_nba)

    game = dbobj.query_dict("SELECT * FROM game WHERE id = %s" % (4356))[0]
    filename = '%s_playbyplay_statsnbacom' % (game['abbrev'])
    obj = Clean(filename, game, dbobj)
    obj.clean()


if __name__ == '__main__':
    main()
