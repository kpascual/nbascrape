import re
import datetime
import sys
import os
import pbp_espn
import shotchart_cbssports

from libscrape.config import constants

LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


def main():
    try:
        dt = sys.argv[1]
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)
        dt = dt.isoformat()
    dt = dt.replace('-','')  
 
    list_files = os.listdir(LOGDIR_EXTRACT)
    list_cbssports = []
    list_espn = []
    list_cbssports_players = []
   
    for l in list_files:
        if re.search('.*%s.*' % dt,l) and re.search('espn',l):
            list_espn.append(l)

        if re.search('.*%s.*' % dt,l) and re.search('_shotchart',l):
            list_cbssports.append(l)

        if re.search('.*%s.*' % dt,l) and re.search('_players',l):
            list_cbssports_players.append(l)

    espn_playbyplay.main(list_espn)
    #cleanCBSSportsPlayers(list_cbssports_players)


def go(tuple_games_and_files):
    for (gamedata,(file_cbssports, file_espn)) in tuple_games_and_files:
        print "+++ Cleaning data in %s" % file_cbssports
        shotvars = {
            'filename':  file_cbssports,
            'home_team': gamedata['home_team'],
            'away_team': gamedata['away_team'],
            'game_name': gamedata['abbrev'],
            'game_id':   gamedata['id'],
            'date_played': gamedata['date_played']
        }
        
        shotchart_cbssports.CleanShots(**shotvars).clean()
        print "Done cleaning shot chart data"

        print "+++ Cleaning data in %s" % file_espn
        pbpvars = {
            'filename':  file_espn,
            'home_team': gamedata['home_team'],
            'away_team': gamedata['away_team'],
            'game_name': gamedata['abbrev'],
            'game_id'  : gamedata['id'],
            'date_played' : gamedata['date_played']
        }
        pbp_espn.Clean(**pbpvars).cleanAll()
        print "Done cleaning play by play data"



if __name__ == '__main__':
    sys.exit(main())
