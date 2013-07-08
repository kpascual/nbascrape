import re
import datetime
import time
import csv
import difflib
import json
import logging

import find_player
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
        self.find_player = find_player.FindPlayer(dbobj)

        # Save the players for each team in this variable -- speed is slow when relying solely on find_player module
        self.players_home = []
        self.players_away = []
        self.players = []
        self.known_plays = []

        self.plays = ''


    def _clean(self):
        self.plays = self._getPlays()

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

        for play in all_plays:
            print play


    def cleanAll(self):
        self.plays = self._getPlays()

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

        logging.info("CLEAN - playbyplay_espn - game_id: %s - play count: %s" % (self.gamedata['id'], len(all_plays)))
        self.dumpIntoFile(all_plays) 


    def _getPlays(self):
        filename = LOGDIR_EXTRACT + self.filename
        data = [line for line in csv.reader(open(filename,'r'),delimiter=',',lineterminator='\n')]

        headers = ['period','play_index','time_left','away_score','home_score','away_play','home_play']
    
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
            # Define the team_id based on whether away or home table cell was filled in
            line['play_desc'] = self._resolvePlayDescription(line['away_play'], line['home_play'])
            if line['play_desc'] == line['home_play']:
                line['team_id'] = self.home_team
            elif line['play_desc'] == line['away_play']:
                line['team_id'] = self.away_team

            line['play_espn_id'], othervars = self._findPlay(line['play_desc'])

            # Check if team_id from description is different than the away/home alignment from the text file
            if 'team_id' in othervars.keys() and othervars['team_id'] != line['team_id']:
                logging.warning("CLEAN - playbyplay_espn - game_id: %s - team_ids found different in play description: play_index: %s" % (self.gamedata['id'], line['play_index']))

            line.update(othervars)
        
            # Remove home/away delineation
            del line['away_play']
            del line['home_play']

            cleaned.append(line)

        return cleaned 

    
    def fillInEmptyFields(self, data):
        newdata = []
        for line in data:
            if 'player_id' not in line.keys():
                line['player_id'] = -1
            if 'assist_player_id' not in line.keys():
                line['assist_player_id'] = -1
            if 'player1_id' not in line.keys():
                line['player1_id'] = -1
            if 'player2_id' not in line.keys():
                line['player2_id'] = -1
            

            newdata.append(line)

        return newdata


    def _resolvePlayDescription(self, away_play_desc, home_play_desc):
        if away_play_desc == '&nbsp;' or away_play_desc == '':
            return home_play_desc
        elif home_play_desc == '&nbsp;' or home_play_desc == '':
            return away_play_desc

        return ''


    def _getKnownPlays(self):
        return self.db.query("SELECT id,re,name FROM play_espn ORDER BY priority ASC, id ASC")


    def _findPlay(self, play):
        if not self.known_plays:
            self.known_plays = self._getKnownPlays()

        for (play_id, play_re, play_name) in self.known_plays:
            
            match = re.match(play_re, play)
            if match:
                othervars = {}
                for key,val in match.groupdict().items():
                    
                    if 'player' in key:
                        player_id = self._identifyPlayer(val.strip())
                        othervars[key + '_id'] = player_id

                    elif 'team' == key:
                        othervars['team_id'] = self._identifyTeam(val.strip())
                    else:
                        othervars[key] = val

                if 'player_id' in othervars and othervars['player_id']  == 0:
                    logging.warning("CLEAN - playbyplay_espn - game_id: %s - player not found in play_name: '%s'" % (self.gamedata['id'], play_name))

                return (play_id, othervars)

        print "No play found: %s" % play
        logging.warning("CLEAN - playbyplay_espn - game_id: %s - no play found: '%s'" % (self.gamedata['id'], play))

        return 0


    def _identifyTeam(self, team_name):
        team = self.db.query("""
            SELECT id 
            FROM team 
            WHERE id IN (%s,%s) 
                AND season = '%s'
                AND (nickname = '%s' OR alternate_nickname = '%s' OR alternate_nickname2 = '%s' OR city = '%s')
        """ % (self.away_team, self.gamedata['season'], self.home_team, team_name, team_name, team_name, team_name))

        if team:
            return team[0][0]
        else:
            return -1


    def _identifyPlayer(self, player_name):
        if not self.players:
            self.players = self.find_player._getPlayersInGame(self.gamedata['id'])
        #print players

        player_id = self.find_player.matchPlayerByNameApproximate(player_name,self.players)

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


def main():
    dbobj = db.Db(db.dbconn_nba)
    game = dbobj.query_dict("SELECT * FROM game WHERE id = 2366")[0]
    obj = Clean(game['abbrev'] + '_playbyplay_espn',game, dbobj)
    obj._clean()


if __name__ == '__main__':
    main()
