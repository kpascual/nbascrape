import csv
import logging
from libscrape.config import db
from libscrape.config import constants 
import libscrape.config.constants



LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class CleanBoxScore:
    def __init__(self, gamedata, dbobj):
        self.gamedata = gamedata
        self.away_team = self.gamedata['away_team_id']
        self.home_team = self.gamedata['home_team_id']
        self.game_name = self.gamedata['abbrev']
        self.game_id = self.gamedata['id']
        self.date_played = self.gamedata['date_played']
        self.db = dbobj

        self.data = [line for line in csv.reader(open(LOGDIR_EXTRACT + self.gamedata['abbrev'] + '_shotchart_cbssports_players','r'),delimiter=',',lineterminator='\n')]


    def _getPlayerIdsInGame(self):
        players = self.db.query_dict("SELECT * FROM player")
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['cbssports_player_id']] = player['id']

        return players_indexed


    def clean(self):
        existing_players = self._getPlayerIdsInGame()

        box_score_data = []
        for (team, cbssports_id, name, jersey, pos, fg, threept, ft, points) in self.data:
            try:
                player_id = existing_players[int(cbssports_id)]
            except:
                print "player id should exist, but surrogate key not found"
                logging.warning("CLEAN - boxscore_cbssports - game_id: %s - cant match player: '%s'" % (self.gamedata['id'],name))
                player_id = -1

            fgm, fga = fg.split('-')
            threeptmade, threeptattempt = threept.split('-')
            ftm, fta = ft.split('-')
            box_score_data.append([self.game_id,player_id, team, fgm, fga, threeptmade, threeptattempt, ftm, fta, points])

        box_score_fields = [['game_id','player_id','team_id','fgm','fga','3ptm','3pta','ftm','fta','points']]
        writer = csv.writer(open(LOGDIR_CLEAN + self.gamedata['abbrev'] + '_boxscore_cbssports','wb'),delimiter=',',lineterminator='\n')
        writer.writerows(box_score_fields + box_score_data)
         

def run(game, filename, dbobj):
    CleanBoxScore(game, dbobj).clean()
