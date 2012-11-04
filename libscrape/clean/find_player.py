import difflib
from libscrape.config import db
from libscrape.config import constants 
import datetime
import logging

#dbobj = db.Db(db.dbconn_nba)

class FindPlayer:

    def __init__(self, dbobj):
        self.dbobj = dbobj


    def identifyPlayerByGame(self, player_tag, player_list, dt, game_id):
        player_id = self._matchPlayerByTag(player_tag, game_id)
        if player_id == 0:
            player_id = self.identifyPlayerByTag(player_tag, player_list, dt)

        return player_id


    def identifyPlayerByTag(self, player_tag, player_list, dt):

        player_id = self.matchPlayerByNameApproximate(player_tag.replace('_',' '), player_list)

        if player_id == 0:
            player_list = self._getRecentPlayers(dt)
            player_id = self.matchPlayerByNameApproximate(player_tag.replace('_',' '), player_list)

        if player_id == 0:
            player_list = self._getAllPlayers()
            player_id = self.matchPlayerByNameApproximate(player_tag.replace('_',' '), player_list)

        if player_id == 0:
            logging.warning("CLEAN - find_player - game_id: ? - cant find player: '%s'" % (player_tag))

        return player_id



    def _matchPlayerByTag(self, player_tag, game_id):
        player_id = 0
        result = self.dbobj.query("""
            SELECT p.id 
            FROM player p 
            WHERE
                nbacom_player_tag = '%s'
        """ % (player_tag))

        if result:
            player_id = result[0][0]

        return player_id
                


    def matchPlayerByNameApproximate(self, player_name, player_list):
        player_id = 0

        player_names = [name.lower() for id, name in player_list]
        player_ids = [id for id, name in player_list]

        match = difflib.get_close_matches(player_name.lower(),player_names,1, 0.8)
        if match:
            player_id = player_ids[player_names.index(match[0])]
            name = match[0]
        else:
            logging.warning("CLEAN - find_player - game_id: ? - cant find player: '%s'" % (player_name))

        return player_id


    def _getPlayersInGame(self, game_id):
        players = self.dbobj.query_dict("""
            SELECT p.id, p.full_name as 'name', p.full_name_alt1, p.full_name_alt2 
            FROM player p
                INNER JOIN player_nbacom_by_game g ON g.nbacom_player_id = p.nbacom_player_id
            WHERE g.game_id = %s
        """ % (game_id))
        return self._transformPlayersToTuples(players)


    def _getTeamPlayerPool(self, team_id):
        players = self.dbobj.query_dict("SELECT id,full_name as 'name',full_name_alt1, full_name_alt2 FROM player WHERE current_team_id = %s" % (team_id))
        return self._transformPlayersToTuples(players)


    def _getRecentPlayers(self, dt):
        players = self.dbobj.query_dict("""
            SELECT p.id,p.full_name as 'name' ,full_name_alt1, full_name_alt2 
            FROM player p 
                INNER JOIN boxscore_nbacom b ON b.player_id = p.id
                INNER JOIN game g ON g.id = b.game_id
            WHERE
                g.date_played BETWEEN '%s' AND '%s'
        """ % (dt - datetime.timedelta(days=30),dt))
        return _transformPlayersToTuples(players)


    def _getAllPlayers(self):
        players = self.dbobj.query_dict("SELECT id,full_name as 'name',full_name_alt1, full_name_alt2  FROM player WHERE id > 0")
        return self._transformPlayersToTuples(players)


    def _transformPlayersToTuples(self, players):
        newdata = []
        for player in players:
            #data[player['id']] = player['name']
            newdata.append((player['id'],player['name']))

            if player['full_name_alt1']:
                newdata.append((player['id'],player['full_name_alt1']))
            if player['full_name_alt2']:
                newdata.append((player['id'],player['full_name_alt2']))
        
        return newdata


