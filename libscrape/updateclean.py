import sys
import datetime
import os

from libscrape.config import db
from libscrape.config import constants
import clean.pbp_espn
import load.update

LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT
LOGDIR_CLEAN = constants.LOGDIR_CLEAN


def chooseGames(game_ids):

    return db.nba_query_dict("SELECT * FROM game WHERE date_played BETWEEN '2011-02-02' AND '2011-02-26'") 
    #return db.nba_query_dict("SELECT * FROM game WHERE id IN (%s)" % ','.join(map(str,game_ids))) 
    
    

def go():
    game_ids = [1]
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
            clean.pbp_espn.Clean(**pbpvars).cleanAll()
            print "Done cleaning play by play data"

            load.update.updatePlayByPlay(f)


if __name__ == '__main__':
    go()

