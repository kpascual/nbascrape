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

        self.home_players = self._getHomePlayers()
        self.away_players = self._getAwayPlayers()


    def clean(self):
        plays = self.getPlayByPlayData()
        self._dumpIntoFile(plays)

        logging.info("CLEAN - playbyplay_nbacom - game_id: %s - play count: %s" % (self.game['id'], len(plays)))


    def getPlayByPlayData(self):
        PLAY_TYPE_NBACOM_SUBSTITUTION = 12
        PLAY_TYPE_NBACOM_JUMPBALL = 18
        PLAY_TYPES_NBACOM_PLAYER2_SAME = [12,14,24,55]

        soup = BeautifulStoneSoup(self.xml)
        playbyplaydata = soup.findAll("event")

        cleaned_plays = []
        for i,play in enumerate(playbyplaydata):
            playdata = dict(play.attrs)
            playdata['play_desc'] = play.contents[0].replace('&lt;![CDATA','').replace(']]&gt;','')
            playdata['deciseconds_left'] = self._transformTimeToTenthSeconds(playdata['game_clock'])

            # Re-key scores
            playdata['game_id'] = self.game['id']
            playdata['home_score'] = playdata['htms']
            playdata['away_score'] = playdata['vtms']
            playdata['period'] = playdata['prd']
            playdata['play_index'] = playdata['eventid']
            playdata.update(self._identifyPlayType(playdata['play_desc']))
            
            if playdata['tm']:
                playdata['team_id'] = self._findTeamId(playdata['tm'])

            
            for pid in ['player_id','player1_id','player2_id']:
                if pid in playdata.keys():
                    # Choose the player list to choose from
                    if playdata['play_type_nbacom_id'] == PLAY_TYPE_NBACOM_JUMPBALL:
                        player_list = self.home_players + self.away_players
                    elif pid == 'player2_id':
                        if playdata['play_type_nbacom_id'] in PLAY_TYPES_NBACOM_PLAYER2_SAME:
                            player_list = self.home_players if playdata['team_id'] == self.game['home_team_id'] else self.away_players
                        else:
                            player_list = self.away_players if playdata['team_id'] == self.game['home_team_id'] else self.home_players
                    else:
                        player_list = self.home_players if playdata['team_id'] == self.game['home_team_id'] else self.away_players

                    # When player2, choose the opposite team, for all plays except assists and subtitutions
                    playdata[pid] = self.find_player.matchPlayerByLastName(playdata[pid],player_list)
                else:
                    playdata[pid] = -1
            

            if playdata['player_code']: 
                player_id = self._resolvePlayers(playdata['player_code'], playdata['team_id'])
                #self._assignToPlayerId(player_id, play_type_nbacom)
                
                if playdata['play_type_nbacom_id'] == PLAY_TYPE_NBACOM_SUBSTITUTION:
                    playdata['player2_id'] = player_id
                else:
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


    def _resolvePlayers(self, player_code, team_id):
        player_pool = []
        if team_id == self.game['home_team_id']:
            player_pool = self.home_players
        elif team_id == self.game['away_team_id']:
            player_pool = self.away_players

        player_pool = self.find_player._transformPlayersToTuples(player_pool)
        return self.find_player.identifyPlayerByGame(player_code, player_pool, self.game['date_played'], self.game['id'])

    
    def _findTeamId(self, name):
        teams = self._getTeams()

        team_id = 0
        for tid, nickname in teams:
            if name == nickname.lower():
                team_id = tid
            if name == nickname.lower():
                team_id = tid

        if team_id == 0:
            logging.warning("CLEAN - playbyplay_nbacom - game_id: %s - cant find team: '%s'" % (self.game['id'], name))

        return team_id


    def _getAwayPlayers(self):
        return self.qry.query_dict("SELECT pnba.player_id, pnba.team_id, pnba.last_name, p.full_name, p.full_name_alt1, p.full_name_alt2 FROM player_nbacom_by_game pnba INNER JOIN player p ON p.id = pnba.player_id WHERE pnba.game_id = %s AND pnba.team_id = %s" % (self.game['id'], self.game['away_team_id']))


    def _getHomePlayers(self):
        return self.qry.query_dict("SELECT pnba.player_id, pnba.team_id, pnba.last_name, p.full_name, p.full_name_alt1, p.full_name_alt2 FROM player_nbacom_by_game pnba INNER JOIN player p ON p.id = pnba.player_id WHERE pnba.game_id = %s AND pnba.team_id = %s" % (self.game['id'], self.game['home_team_id']))


    def _convertToDict(self, data, key):
        newdata = []
        for line in data:
            newdata.append((line[key],dict([(k,v) for k, v in line.items() if k != key])))
        
        return dict(newdata)


    def _getTeams(self):
        teams = self.qry.query_dict("""
            SELECT id, nickname, alternate_nickname, alternate_nickname2 
            FROM team 
            WHERE id IN (%s,%s)
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

    game = dbobj.query_dict("SELECT * FROM game WHERE id = %s" % (2734))[0]
    filename = '%s_playbyplay_nbacom' % (game['abbrev'])
    obj = Clean(filename,game,dbobj)
    data = obj.getPlayByPlayData()
    #for row in data:
    #    print dict([(key,val) for key,val in row.items() if 'player' in key or 'play_desc' in key])


if __name__ == '__main__':
    main()
