import re
import datetime
import time
import json
from BeautifulSoup import BeautifulStoneSoup
import find_player
import logging

from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT
LOGDIR_SOURCE = constants.LOGDIR_SOURCE



# action_type: 1 = made, 2 = missed
# msg_type:

class Clean:

    def __init__(self, filename, gamedata, dbobj):
        self.xml = open(LOGDIR_SOURCE + filename,'r').read()
        self.qry = dbobj
        self.dbobj = dbobj
        self.game = gamedata
        self.filename = filename
        self.find_player = find_player.FindPlayer(dbobj)


    def clean(self):
        plays = self.getPlayByPlayData()
        self._dumpIntoFile(plays)

        logging.info("CLEAN - playbyplay_nbacom - game_id: %s - play count: %s" % (self.game['id'], len(plays)))


    def getPlayByPlayData(self):
        soup = BeautifulStoneSoup(self.xml)
        playbyplaydata = soup.findAll("event")

        # Get team nicknames
        teams = self._getTeams()

        # Find player
        home_players = self.find_player._getTeamPlayerPool(self.game['home_team_id'])
        away_players = self.find_player._getTeamPlayerPool(self.game['away_team_id'])

        cleaned_plays = []
        for i,play in enumerate(playbyplaydata):
            playdata = dict(play.attrs)
            playdata['play_desc'] = play.contents[0].replace('&lt;![CDATA','').replace(']]&gt;','')
            playdata['deciseconds_left'] = self._transformTimeToTenthSeconds(playdata['game_clock'])

            # Re-key scores
            playdata['home_score'] = playdata['htms']
            playdata['away_score'] = playdata['vtms']
            playdata['period'] = playdata['prd']
            playdata['play_index'] = playdata['eventid']
            playdata.update(self._identifyPlayType(playdata['play_desc']))

            playdata['game_id'] = self.game['id']
            
            if playdata['tm']:
                team_id = 0
                for tid, nickname in teams:
                    if playdata['tm'] == nickname.lower():
                        team_id = tid
                    if playdata['tm'] == nickname.lower():
                        team_id = tid

                if team_id == 0:
                    logging.warning("CLEAN - playbyplay_nbacom - game_id: %s - cant find team: '%s'" % (self.game['id'], playdata['tm']))

                playdata['team_id'] = team_id

            if playdata['player_code']: 
                player_pool = []
                if playdata['team_id'] == self.game['home_team_id']:
                    player_pool = home_players
                elif playdata['team_id'] == self.game['away_team_id']:
                    player_pool = away_players

                player_id = self.find_player.identifyPlayerByGame(playdata['player_code'], player_pool, self.game['date_played'], self.game['id'])
                #print player_id
                playdata['player_id'] = player_id

            # Delete extraneous keys
            del playdata['tm']
            del playdata['eventid']
            del playdata['player_code']
            del playdata['htms']
            del playdata['vtms']
            del playdata['prd']
            del playdata['game_clock']
        
            cleaned_plays.append(playdata)

        return cleaned_plays


    def _transformTimeToTenthSeconds(self, game_clock):

        mins, secs = game_clock.split(':')
        total_secs = int(mins)*60*10 + int(float(secs) * 10)

        return total_secs


    def resolvePlayer(self, player_code):
        pass

    


    def _resolveTeam(self, nbacom_team_code):
        team = self.qry.query("SELECT * FROM team WHERE nbacom_code = '%s'" % (nbacom_team_code))
        return team[0][0]



    def _getTeams(self):
        teams = self.qry.query_dict("""
            SELECT id, nickname, alternate_nickname, alternate_nickname2 
            FROM team 
            WHERE is_active = 1 AND id IN (%s,%s)
        """ % (self.game['home_team_id'],self.game['away_team_id']))
    
        data = []
        for team in teams:
            data.append((team['id'],team['nickname']))

            if team['alternate_nickname']:
                data.append((team['id'],team['alternate_nickname']))
            if team['alternate_nickname']:
                data.append((team['id'],team['alternate_nickname2']))

        return data


    def _identifyPlayType(self, play):
        #'&lt;![CDATA[(00:00.0)[POR] Team Rebound]]&gt;'

        patterns = self.dbobj.query("SELECT id, re FROM play_type_nbacom ORDER BY priority ASC")

        for i,pattern in patterns:
            match = re.match(pattern, play)
            if match:
                
                values = match.groupdict()
                values['play_type_nbacom_id'] = i

                return values

        logging.warning("CLEAN - playbyplay_nbacom - game_id: %s - cant match play: '%s'" % (self.game['id'], play))

        return {'play_type_nbacom_id':-1}


    def _dumpIntoFile(self, data):
        f = open(LOGDIR_CLEAN + self.filename,'wb')
        f.write(json.dumps(data))


# I think msg_type is actually play_type
# And I think action_type is really just the shot type
def main():

    dbobj = db.Db(db.dbconn_nba)
    for id in range(2171,2172):
        game = dbobj.query_dict("SELECT * FROM game WHERE id = %s" % (id))[0]
        filename = '%s_playbyplay_nbacom' % (game['abbrev'])
        obj = Clean(filename,game,dbobj)
        
        plays = obj.getPlayByPlayData()
        #obj._dumpIntoFile(plays)
        for play in plays:
            #print (play['action_type'],play['play_type_nbacom_id'])
            print play


if __name__ == '__main__':
    main()
