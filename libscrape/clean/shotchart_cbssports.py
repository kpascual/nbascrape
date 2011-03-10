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
    def __init__(self, filename, away_team, home_team, game_name, game_id, date_played):
        self.filename = filename
        self.away_team = away_team
        self.home_team = home_team
        self.game_name = game_name
        self.game_id = game_id
        self.date_played = date_played

        self.players = [line.rstrip().split(',') for line in open(LOGDIR_EXTRACT + self.filename + '_players','r').readlines()]
        self.existing_players = dict(self._getExistingPlayers())
        self.player_surrogates = self.identifyPlayers()
        self.shots = [line.rstrip().split(',') for line in open(LOGDIR_EXTRACT + self.filename + '_shots','r').readlines()]

        self.finalfields = ['shot_num','team_code','sec_elapsed_game','period','player_id',
                            'shot_type_id','result','x','y','distance','game_id']

    def clean(self):

        cleaned = []
        cleaned1 = self.adjustFourthPeriod(self.shots)
        cleaned2 = self.replaceWithConformedTime(cleaned1)
        cleaned3 = self.adjustTeam(cleaned2)
        cleaned4 = self.adjustPlayer(cleaned3)
        cleaned5 = self.addGameId(cleaned4)

        # Dump box score data
        self.makePlayerBoxScore()

        self._dumpIntoFile(cleaned5)

    
    def _dumpIntoFile(self, plays):
        
        writer = csv.writer(open(LOGDIR_CLEAN + self.filename,'wb'),delimiter=',',lineterminator='\n')
        writer.writerows([self.finalfields] + plays)
        

    def adjustFourthPeriod(self, data):

        cleaned = []
        last_period = 1
        current_period = 1
        last_seconds = 721
        for counter, (i,team,time_left,period,player_id,shot_type,result,x,y,distance) in enumerate(data):

            new_time = time_left.split(':')
            if len(new_time) == 2:
                new_seconds = int((lambda x,y: int(x)*60 + int(y))(*new_time))
            else:
                new_seconds = int(time_left.split('.')[0])

            if last_seconds < new_seconds and new_seconds - last_seconds > 150:
                if int(last_period) >= 3:
                    current_period = current_period + 1
                else:
                    current_period = int(period)
 
            last_period = current_period
            last_seconds = new_seconds
            

            cleaned.append((i,team,new_seconds,current_period,player_id,shot_type,result,x,y,distance))

        return cleaned


    def _getConformedTime(self):
        return db.nba_query_dict("SELECT * FROM dim_times")


    def replaceWithConformedTime(self, plays):
        conformed_times = self._getConformedTime()
        cleaned = []
        for (i,team,time_left,period,player_id,shot_type,result,x,y,distance) in plays:
            try:
                found = [itm['sec_elapsed_game'] for itm in conformed_times if itm['period'] == period and itm['sec_left_period'] == time_left][0]
                time_elapsed = found
            except:
                logger.warn("time not found! period: %s, time: %s, counter: %s" % (period,time_left,i))
                time_elapsed = -1

            cleaned.append((i,team,time_elapsed,period,player_id,shot_type,result,x,y,distance))

        return cleaned


    def adjustTeam(self, data):
        cleaned = []
        for i,team,time_left,period,player_id,shot_type,result,x,y,distance in data:
            if int(team) == 0:
                team = self.away_team
            else:
                team = self.home_team
            
            cleaned.append((i,team,time_left,period,player_id,shot_type,result,x,y,distance))

        return cleaned


    def adjustPlayer(self, data):
        cleaned = []
        for i,team,time_left,period,player_id,shot_type,result,x,y,distance in data:
            try:
                new_player_id = self.existing_players[int(player_id)][0]
            except:
                new_player_id = 0
                logger.warn("Could not find player %s" % player_id)

            cleaned.append((i,team,time_left,period,new_player_id,shot_type,result,x,y,distance))

        return cleaned 


    def identifyPlayers(self):
        cleaned = []
        for (team, cbssports_id, name, jersey, pos, fg, threept, ft, points) in self.players:
            isCBSSportsIdExists = int(cbssports_id) in self.existing_players.keys() 
             
            if not isCBSSportsIdExists:  
                ins = """
                    INSERT INTO player (team_code, full_name, cbssports_player_id, jersey, position, start_date) 
                    VALUES ('%s','%s',%s,'%s','%s','%s')
                """ % (team,name.replace('&nbsp;',' ').replace('&#039;',"\\'"),cbssports_id,jersey,pos,self.date_played)
                logger.info("Adding %s to player list (team: %s, cbssports_id %s" % (name, team, cbssports_id))
                curs = db.nba_curs()
                curs.execute(ins)
                cleaned.append((cbssports_id, curs.lastrowid))
            elif isCBSSportsIdExists and self.existing_players[int(cbssports_id)][2] != team:
                #Add end date to current player id
                old_id = self.existing_players[int(cbssports_id)][0]

                curs = db.nba_curs()
                curs.execute("UPDATE player SET end_date = '%s' WHERE id = %s" % (self.date_played, old_id))
                ins = """
                    INSERT INTO player (team_code, full_name, cbssports_player_id, jersey, position, start_date) 
                    VALUES ('%s','%s',%s,'%s','%s','%s')
                """ % (team,name.replace('&nbsp;',' '),cbssports_id,jersey,pos,self.date_played)
                logger.info("Adding %s to player list (team: %s, cbssports_id %s" % (name, team, cbssports_id))
                curs.execute(ins)
                cleaned.append((cbssports_id, curs.lastrowid))

            else:
                surrogate = self.existing_players[int(cbssports_id)][0]
                cleaned.append((cbssports_id, surrogate))
                #print "correctly identified %s as %s: %s" % (cbssports_id, name, self.existing_players[int(cbssports_id)][0])

        self.existing_players = dict(self._getExistingPlayers())
        return cleaned

  
    def _getExistingPlayers(self):
        result = db.nba_query("""
            SELECT cbssports_player_id, id, full_name, team_code 
            FROM player 
            WHERE start_date <= '%s' and (end_date >= '%s' OR end_date IS NULL)
                AND  team_code IN ('%s','%s')
        """ % (self.date_played, self.date_played, self.away_team, self.home_team))
        return dict([(line[0], line[1:]) for line in result])


    def makePlayerBoxScore(self):
        box_score_data = []
        
        for (team, cbssports_id, name, jersey, pos, fg, threept, ft, points) in self.players:
            try:
                surrogate_player_id = self.existing_players[int(cbssports_id)][0]
            except:
                print "player id should exist, but surrogate key not found"
                surrogate_player_id = -1

            fgm, fga = fg.split('-')
            threeptmade, threeptattempt = threept.split('-')
            ftm, fta = ft.split('-')
            box_score_data.append([self.game_id,surrogate_player_id, team, fgm, fga, threeptmade, threeptattempt, ftm, fta, points])

        box_score_fields = [['game_id','player_id','team_code','fgm','fga','3ptm','3pta','ftm','fta','points']]
        writer = csv.writer(open(LOGDIR_CLEAN + self.filename + '_boxscore','wb'),delimiter=',',lineterminator='\n')
        writer.writerows(box_score_fields + box_score_data)
         

    def swapForSurrogate(self, data):
        for (i,team,time_left,quarter,player_id,shot_type,result,x,y,distance) in data:
            # Swap team name
            if team == 0:
                team = self.away_team
            else:
                team = self.home_team


    def addGameId(self, data):
        cleaned = []
        for tup in data:
            new = list(tup) + [self.game_id]
            cleaned.append(new)

        return cleaned


