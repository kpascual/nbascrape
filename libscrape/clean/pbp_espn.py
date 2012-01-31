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

        self.known_plays = self._getKnownPlays()
        #self.plays = [line.replace('\n','').split(',') for line in open(LOGDIR_EXTRACT + filename,'r').readlines()]
        self.plays = [line for line in csv.reader(open(LOGDIR_EXTRACT + filename,'r'),delimiter=',',lineterminator='\n')]
        self.fields = ['game_id', 'assist_player_id', 'away_score', 'distance', 'foul_info', 'foul_type', 'home_score', 'period', 'play_id', 'play_num', 'player1_id', 'player2_id', 'player_id', 'sec_elapsed_game', 'shot_type', 'team_id','home_play_desc','away_play_desc','play_desc']


    def cleanAll(self):
        cleaning_functions = [
            self.guessUnknownQuarters,
            self.replaceBlankScores,
            self.replaceWithConformedTime,
            self.identifyPlays
        ]

        all_plays = self.plays
        for function_name in cleaning_functions:
            all_plays = function_name(all_plays)
      
        self.dumpIntoFile(all_plays) 
        #self.tempDbInsert(cleaned4) 


    def tempDbInsert(self, data):
        for line in data:
            sql = "INSERT INTO pbptest (%s) VALUES (%s)" % (','.join(line.keys()),"'%s'" % "','".join(map(str,line.values())))
            self.db.query(sql)


    def guessUnknownQuarters(self, plays):
        newdata = []
        for i, line in enumerate(plays):
            if line[0] == 'check quarter':
                line[0] = self.plays[i-1][0]
            
            newdata.append(line)

        return newdata
    

    def _getConformedTimes(self):
        return self.db.query_dict("SELECT * FROM dim_times")


    def replaceWithConformedTime(self, plays):
        #conformed_times = self._getConformedTimes()
        cleaned = []
        for (period, idx, time_left, away_score, home_score, away_play, home_play) in plays:
            #found = [(itm['period'], itm['sec_elapsed_game']) for itm in conformed_times if itm['period_name'] == period and itm['time_left'] == time_left][0]
            #period = found[0]
            #time_left = found[1]
            new_time_left = (int(time_left.split(':')[0]) * 60 + int(time_left.split(':')[1])) * 10
            cleaned.append((period, idx, new_time_left, away_score, home_score, away_play, home_play)) 
    
        return cleaned


    def replaceBlankScores(self, data):
        new = []
        for i, line in enumerate(data):
            if line[3] == '':
                line[3] = data[i-1][3]
            if line[4] == '':
                line[4] = data[i-1][4]
           
            new.append(line) 

        return new


    def identifyPlays(self, plays):
        cleaned = []
        for (period, idx, time_left, away_score, home_score, away_play, home_play) in plays:
            team, play, othervars = self._findPlay(away_play, home_play)
 
            newline = dict([(f,'') for f in self.fields]) 
            newline.update([('period',period),('play_num',idx),('sec_elapsed_game',time_left),
                ('game_id',self.game_id),('away_score',away_score),('home_score',home_score),('play_id',play),
                ('team_id',team),('home_play_desc',home_play),('away_play_desc',away_play)])
            newline.update(othervars)

            newline['play_desc'] = self._resolvePlayDescription(away_play, home_play)
            cleaned.append(newline)

        return cleaned 


    def _resolvePlayDescription(self, away_play_desc, home_play_desc):
        if away_play_desc == '&nbsp;':
            return home_play_desc
        elif home_play_desc == '&nbsp;':
            return away_play_desc

        return ''


    def _getKnownPlays(self):
        return self.db.query("SELECT id,re,name FROM play_espn ORDER BY priority ASC, id ASC")


    def _findPlay(self,away_play,home_play):
        for (play_id, play_re, play_name) in self.known_plays:
            
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
            FROM player_resolved_test p
                INNER JOIN player_nbacom_by_game g ON g.nbacom_player_id = p.nbacom_player_id
            WHERE g.game_id = %s
        """ % (self.gamedata['id']))
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['id']] = player['first_name'] + " " + player['last_name']

        return players_indexed


    def dumpIntoFile(self, data):
        writer = csv.writer(open(LOGDIR_CLEAN + self.filename,'wb'),delimiter=',',lineterminator='\n')
        writer.writerows([sorted(self.fields)] + [[val[1] for val in sorted(line.items())] for line in data])


if __name__ == '__main__':
    main()
