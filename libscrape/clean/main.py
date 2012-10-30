import re
import datetime
import time
import sys
import os
import logging

import pbp_espn
import pbp_nbacom
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

        print "+++ CLEAN: %s - %s" % (gamedata['id'], gamedata['abbrev'])

        print "  + Player database"
        obj = player.PlayerNbaCom(LOGDIR_EXTRACT + filenames['boxscore_nbacom'], gamedata, dbobj)
        obj.resolveNewPlayers()
        obj = player.PlayerCbsSports(LOGDIR_EXTRACT + filenames['shotchart_cbssports'] + '_players', gamedata, dbobj)
        obj.resolveNewPlayers()
        player.updatePlayerFullName(dbobj)


        print "  + CBSSports.com shot chart data"
        step_time = time.time()
        shotvars = {
            'filename':  filenames['shotchart_cbssports'],
            'gamedata':  gamedata,
            'dbobj'   :  dbobj
        }
        shotchart_cbssports.CleanShots(**shotvars).clean()
        logging.info("CLEAN - shotchart_cbssports - game_id: %s - : time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))

        print "  + CBSSports.com boxscore data" 
        step_time = time.time()
        boxscore_cbssports.CleanBoxScore(gamedata, dbobj).clean()
        logging.info("CLEAN - boxscore_cbssports - game_id: %s - : time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))

        print "  + NBA.com boxscore data" 
        step_time = time.time()
        boxscore_nbacom.CleanBoxScore(filenames['boxscore_nbacom'],gamedata, dbobj).clean()
        logging.info("CLEAN - boxscore_nbacom - game_id: %s - : time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))

        print "  + NBA.com play by play data" 
        step_time = time.time()
        pbp_nbacom.Clean(filenames['playbyplay_nbacom'],gamedata, dbobj).clean()
        logging.info("CLEAN - playbyplay_nbacom - game_id: %s - : time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))

        print "  + ESPN play by play data"
        step_time = time.time()
        pbpvars = {
            'filename':  filenames['playbyplay_espn'],
            'gamedata':  gamedata,
            'dbobj'   :  dbobj
        }
        pbp_espn.Clean(**pbpvars).cleanAll()
        logging.info("CLEAN - playbyplay_espn - game_id: %s - : time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))

        print "  + NBA.com shot chart data"
        step_time = time.time()
        shotchart_nbacom.Clean(filenames['shotchart_nbacom'],gamedata, dbobj).cleanAll()
        logging.info("CLEAN - shotchart_nbacom - game_id: %s - : time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))

        print "  + ESPN.com shot chart data"
        step_time = time.time()
        shotchart_espn.Clean(filenames['shotchart_espn'],gamedata, dbobj).cleanAll()
        logging.info("CLEAN - shotchart_espn - game_id: %s - : time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))


if __name__ == '__main__':
    sys.exit(main())
