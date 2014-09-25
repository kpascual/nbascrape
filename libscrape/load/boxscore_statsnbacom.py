import json
from libscrape.config import constants

LOGDIR_CLEAN = constants.LOGDIR_CLEAN

def run(filename, dbobj):
    data = json.loads(open(LOGDIR_CLEAN + filename, 'r').read())
    dbobj.insert_or_update('boxscore_statsnbacom', data)

    stats = json.loads(open(LOGDIR_CLEAN + filename + '_game_stats', 'r').readline())
    dbobj.insert_or_update('game_stats_statsnbacom', stats)

    stats_team = json.loads(open(LOGDIR_CLEAN + filename + '_game_stats_team', 'r').readline())
    dbobj.insert_or_update('game_stats_team_statsnbacom', stats_team)
