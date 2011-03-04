import sys
import datetime
import os

from libscrape.config import db
import pbp_espn
import shotchart_cbssports
import main

LOGDIR_SOURCE = '../../logs/source/'
LOGDIR_EXTRACT = '../../logs/extract/'
LOGDIR_CLEAN = '../../logs/clean/'


def chooseGames(game_ids):

    return db.nba_query_dict("SELECT * FROM game WHERE id IN (%s)" % ','.join(map(str,game_ids))) 
    
    

def go(game_ids):

    game_ids = [250]
    games = chooseGames(game_ids)

    for g in games:
        files_in_extract = [f for f in os.listdir(LOGDIR_EXTRACT) if g['abbrev'] in f and 'espn' in f]
        print files_in_extract

        if files_in_extract:
            f = files_in_extract[0]

            print "+++ Cleaning data in %s" % f
            pbpvars = {
                'filename':  f,
                'home_team': g['home_team'],
                'away_team': g['away_team'],
                'game_name': g['abbrev'],
                'game_id'  : g['id']
            }
            pbp_espn.Clean(**pbpvars).cleanAll()
            print "Done cleaning play by play data"




