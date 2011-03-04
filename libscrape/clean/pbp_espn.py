import re
import datetime
import logging
import logging.config
import csv

from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("play")



class Clean:

    def __init__(self, filename, home_team, away_team, game_name, game_id):
        self.filename = filename
        self.away_team = away_team
        self.home_team = home_team
        self.game_name = game_name
        self.game_id = game_id

        self.known_plays = self._getKnownPlays()
        self.existing_players = self._getExistingPlayers()
        self.plays = [line.replace('\n','').split(',') for line in open(LOGDIR_EXTRACT + filename,'r').readlines()]
        self.fields = ['game_id', 'assist_player_id', 'away_score', 'distance', 'foul_info', 'foul_type', 'home_score', 'period', 'play_id', 'play_num', 'player1_id', 'player2_id', 'player_id', 'sec_elapsed_game', 'shot_type', 'team_code']


    def cleanAll(self):
        cleaned1 = self.guessUnknownQuarters(self.plays)
        cleaned2 = self.replaceBlankScores(cleaned1)
        cleaned3 = self.replaceWithConformedTime(cleaned2)
        cleaned4 = self.identifyPlays(cleaned3)
      
        self.dumpIntoFile(cleaned4) 
        #self.tempDbInsert(cleaned4) 


    def tempDbInsert(self, data):
        for line in data:
            sql = "INSERT INTO pbptest (%s) VALUES (%s)" % (','.join(line.keys()),"'%s'" % "','".join(map(str,line.values())))
            db.nba_query(sql)


    def guessUnknownQuarters(self, plays):
        newdata = []
        for i, line in enumerate(plays):
            if line[0] == 'check quarter':
                line[0] = self.plays[i-1][0]
            
            newdata.append(line)

        return newdata
    

    def _getConformedTimes(self):
        return db.nba_query_dict("SELECT * FROM dim_times")


    def replaceWithConformedTime(self, plays):
        conformed_times = self._getConformedTimes()
        cleaned = []
        for (period, idx, time_left, away_score, home_score, away_play, home_play) in plays:
            found = [(itm['period'], itm['sec_elapsed_game']) for itm in conformed_times if itm['period_name'] == period and itm['time_left'] == time_left][0]
            period = found[0]
            time_left = found[1]
            cleaned.append((period, idx, time_left, away_score, home_score, away_play, home_play)) 
    
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
            team, play, othervars = self.findPlay(away_play, home_play)
 
            newline = dict([(f,'') for f in self.fields]) 
            newline.update([('period',period),('play_num',idx),('sec_elapsed_game',time_left),
                ('game_id',self.game_id),('away_score',away_score),('home_score',home_score),('play_id',play),
                ('team_code',team)])
            newline.update(othervars)


            cleaned.append(newline)

        return cleaned 


    def _getKnownPlays(self):
        return db.nba_query("SELECT id,re,name FROM play ORDER BY priority ASC, id ASC")


    def findPlay(self,away_play,home_play):
        for (play_id, play_re, play_name) in self.known_plays:
            match = re.search(play_re,away_play)
            if match:
                othervars = {}
                for key,val in match.groupdict().items():
                    
                    if 'player' in key:
                        othervars[key + '_id'] = self._identifyPlayer(val, self.away_team)
                    else:
                        othervars[key] = val

                return (self.away_team, play_id, othervars)

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
        logger.info("No play found: %s" % play)
        return 0


    def _identifyPlayer(self, player_name, team):
        # If player name ends in an "apostrophe s ('s)", then strip out apostrophe and "s"

        for (id, team_code, full_name, alternate_name) in self.existing_players:
            if full_name == player_name and team == team_code:
                return id
            elif alternate_name == player_name and team == team_code:
                return id
            elif full_name == player_name:
                # Just in case I'm looking at the wrong team
                return id 

        logger.warn("Could not detect player name: '%s'" % player_name)
        curs = db.nba_curs()
        #curs.execute("INSERT INTO player (full_name) VALUES ('%s')" % player_name)
        #return curs.lastrowid


    def _getExistingPlayers(self):
        return db.nba_query("SELECT id, team_code, full_name, alternate_name FROM player WHERE team_code IN ('%s','%s')" % (self.home_team, self.away_team))
        

    def dumpIntoFile(self, data):
        writer = csv.writer(open(LOGDIR_CLEAN + self.filename,'wb'),delimiter=',',lineterminator='\n')
        writer.writerows([sorted(self.fields)] + [[val[1] for val in sorted(line.items())] for line in data])


    def createFiveManUnits(self):
        pass


if __name__ == '__main__':
    main()
