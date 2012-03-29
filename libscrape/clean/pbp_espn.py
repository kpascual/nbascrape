import re
import datetime
import csv
import difflib
import json

from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT




class Clean:

    def __init__(self, filename, gamedata, dbobj):
        self.filename = filename
        self.gamedata = gamedata
        self.away_team = self.gamedata['away_team_id']
        self.home_team = self.gamedata['home_team_id']
        self.game_name = self.gamedata['abbrev']
        self.game_id = self.gamedata['id']
        self.date_played = self.gamedata['date_played']
        self.db = dbobj

        #self.plays = [line.replace('\n','').split(',') for line in open(LOGDIR_EXTRACT + filename,'r').readlines()]
        self.plays = self._getPlays()


    def cleanAll(self):
        cleaning_functions = [
            self.guessUnknownQuarters,
            self.replaceBlankScores,
            self.replaceWithConformedTime,
            self.addGameId,
            self.identifyPlays,
            self.fillInEmptyFields
        ]

        all_plays = self.plays
        for function_name in cleaning_functions:
            all_plays = function_name(all_plays)

        self.dumpIntoFile(all_plays) 


    def _getPlays(self):
        filename = LOGDIR_EXTRACT + self.filename
        data = [line for line in csv.reader(open(filename,'r'),delimiter=',',lineterminator='\n')]

        headers = ['period','play_num','time_left','away_score','home_score','away_play','home_play']
    
        newdata = []
        for line in data:
            newline = dict(zip(headers,line))
            newdata.append(newline)

        return newdata


    def guessUnknownQuarters(self, plays):
        newdata = []
        for i, line in enumerate(plays):
            if line['period'] == 'check quarter':
                line['period'] = plays[i-1]['period']
            
            newdata.append(line)

        return newdata
    

    def _getConformedTimes(self):
        return self.db.query_dict("SELECT * FROM dim_times")


    def replaceWithConformedTime(self, plays):
        #conformed_times = self._getConformedTimes()
        cleaned = []
        for line in plays:
        #for (period, idx, time_left, away_score, home_score, away_play, home_play) in plays:
            #found = [(itm['period'], itm['deciseconds_left']) for itm in conformed_times if itm['period_name'] == period and itm['time_left'] == time_left][0]
            #period = found[0]
            #time_left = found[1]
            line['deciseconds_left'] = (int(line['time_left'].split(':')[0]) * 60 + int(line['time_left'].split(':')[1])) * 10
            del line['time_left']

            cleaned.append(line)
            #cleaned.append((period, idx, new_time_left, away_score, home_score, away_play, home_play)) 
    
        return cleaned


    def replaceBlankScores(self, data):
        new = []
        for i, line in enumerate(data):
            if line['away_score'] == '':
                line['away_score'] = data[i-1]['away_score']
            if line['home_score'] == '':
                line['home_score'] = data[i-1]['home_score']
           
            new.append(line) 

        return new


    def addGameId(self, data):
        new = []
        for i, line in enumerate(data):
            line['game_id'] = self.game_id
            new.append(line) 

        return new


    def identifyPlays(self, plays):
        cleaned = []
        for line in plays:
        #for (period, idx, time_left, away_score, home_score, away_play, home_play) in plays:
            team_id, play_espn_id, othervars = self._findPlay(line['away_play'], line['home_play'])

            line['play_espn_id'] = play_espn_id
            line['team_id'] = team_id
            line['play_desc'] = self._resolvePlayDescription(line['away_play'], line['home_play'])
            line.update(othervars)

            del line['away_play']
            del line['home_play']

            cleaned.append(line)

        return cleaned 

    
    def fillInEmptyFields(self, data):
        newdata = []
        for line in data:
            if 'assist_player_id' not in line.keys():
                line['assist_player_id'] = -1
            if 'player1_id' not in line.keys():
                line['player1_id'] = -1
            if 'player2_id' not in line.keys():
                line['player2_id'] = -1
            

            newdata.append(line)

        return newdata


    def _resolvePlayDescription(self, away_play_desc, home_play_desc):
        if away_play_desc == '&nbsp;':
            return home_play_desc
        elif home_play_desc == '&nbsp;':
            return away_play_desc

        return ''


    def _getKnownPlays(self):
        return self.db.query("SELECT id,re,name FROM play_espn ORDER BY priority ASC, id ASC")


    def _findPlay(self,away_play,home_play):
        known_plays = self._getKnownPlays()
        for (play_id, play_re, play_name) in known_plays:
            
            # Identify away play
            match = re.search(play_re,away_play)
            if match:
                othervars = {}
                for key,val in match.groupdict().items():
                    
                    if 'player' in key:
                        othervars[key + '_id'] = self._identifyPlayer(val, self.away_team)
                    else:
                        othervars[key] = val

                return (self.away_team, play_id, othervars)

            # Identify home play
            match = re.search(play_re,home_play)
            if match:
                othervars = {}
                for key,val in match.groupdict().items():
                    if 'player' in key:
                        othervars[key + '_id'] = self._identifyPlayer(val, self.home_team)
                    else:
                        othervars[key] = val

                return (self.home_team, play_id, othervars)

        print "No play found: %s" % play
        return 0



    def _identifyPlayer(self, player_name, team):
        players = self._getPlayerIdsInGame()
        player_names = [name for player_id, name in sorted(players.items())]
        player_ids = [player_id for player_id, name in sorted(players.items())]

        match = difflib.get_close_matches(player_name,player_names,1, 0.8)
        if match:
            player_id = player_ids[player_names.index(match[0])]
        else:
            player_id = 0

        return player_id


    def _getPlayerIdsInGame(self):
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


    def dumpIntoFile(self, data):
        f = open(LOGDIR_CLEAN + self.filename,'wb')
        f.write(json.dumps(data))


if __name__ == '__main__':
    main()
