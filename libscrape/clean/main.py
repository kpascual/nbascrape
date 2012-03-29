import re
import datetime
import sys
import os
import pbp_espn
import shotchart_cbssports
import shotchart_espn
import shotchart_nbacom
import boxscore_cbssports
import boxscore_nbacom
import player

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


def go(tuple_games_and_files, dbobj):

    for gamedata,filenames in tuple_games_and_files:

        print "+++ Resolving master player database"
        obj = player.PlayerNbaCom(LOGDIR_EXTRACT + filenames['boxscore_nbacom'], gamedata, dbobj)
        obj.resolveNewPlayers()
        obj = player.PlayerCbsSports(LOGDIR_EXTRACT + filenames['shotchart_cbssports'] + '_players', gamedata, dbobj)
        obj.resolveNewPlayers()
        player.updatePlayerFullName(dbobj)


        print "+++ Cleaning CBSSports.com shot chart data in %s" % (filenames['shotchart_cbssports'])
        shotvars = {
            'filename':  filenames['shotchart_cbssports'],
            'gamedata':  gamedata,
            'dbobj'   :  dbobj
        }
        
        shotchart_cbssports.CleanShots(**shotvars).clean()
        print "+++ Done cleaning CBSSports.com shot chart data"

        print "+++ Creating CBSSports.com boxscore data" 
        boxscore_cbssports.CleanBoxScore(gamedata, dbobj).clean()
        print "+++ Done cleaning CBSSports.com shot chart data"

        print "+++ Creating NBA.com boxscore data" 
        boxscore_nbacom.CleanBoxScore(filenames['boxscore_nbacom'],gamedata, dbobj).clean()
        print "+++ Done cleaning NBA.com shot chart data"

        print "+++ Cleaning ESPN play by play data in %s" % (filenames['playbyplay_espn'])
        pbpvars = {
            'filename':  filenames['playbyplay_espn'],
            'gamedata':  gamedata,
            'dbobj'   :  dbobj
        }
        pbp_espn.Clean(**pbpvars).cleanAll()
        print "+++ Done cleaning ESPN play by play data"

        print "+++ Cleaning NBA.com shot chart data in %s" % (filenames['shotchart_nbacom'])
        shotchart_nbacom.Clean(filenames['shotchart_nbacom'],gamedata, dbobj).cleanAll()
        print "+++ Done"

        print "+++ Cleaning ESPN.com shot chart data in %s" % (filenames['shotchart_espn'])
        shotchart_espn.Clean(filenames['shotchart_espn'],gamedata, dbobj).cleanAll()
        print "+++ Done"


if __name__ == '__main__':
    sys.exit(main())
