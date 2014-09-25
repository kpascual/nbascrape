import sys
import time
import datetime
import MySQLdb
import os
import logging

from libscrape.config import constants
import configg
import league
import source.main
import extract.main
import clean.main
import load.main


LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

logging.basicConfig(filename='etl.log',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


class Scrape:
    def __init__(self, dbobj, league):
        league_map = {
            'nba': 1,
            'wnba': 2,
            'fiba': 3
        }
        self.league = league
        self.league_season_id = self._getLeagueSeason({league_id: league_map[league]})


    def _scrape(self):
        pass


    def run(self):
        pass

    def _getLeagueSeason(self, params):
        pass

    def _getModules(self):
        module_map = {
            'nba': [
                'boxscore_nbacom',
                'boxscore_cbssports',
                'playbyplay_espn',
                'playbyplay_nbacom',
                'shotchart_cbssports',
                'shotchart_espn',
                'shotchart_nbacom',
                'playbyplay_statsnbacom',
                'shotchart_statsnbacom',
                'boxscore_statsnbacom'
            ],
            'wnba': [
                'boxscore_nbacom',
                'playbyplay_espn',
                'playbyplay_nbacom',
                'shotchart_espn',
                'shotchart_wnbacom'
            ]    
            
        }

        return module_map(self.league)



def scrapeAuto(league_name, dt, files = None):
    step_time = time.time()

    config_no_pw = configg.dbobj.getCredentials()
    

    # MAIN ETL PROCESS
    print "+++ MASTER ETL - league: %s - database: %s" % (league_name, config_no_pw)
    logging.info("MASTER - starting ETL job - league: %s - date: %s - database: %s" % (league_name, dt, config_no_pw))

    scrape(configg.dbobj, league_name, dt, files)

    time_elapsed = "Total time: %.2f sec" % (time.time() - step_time)
    logging.info(time_elapsed)


def scrape(dbobj, league_name, dt, files):
    if not files:
        files = [
            'boxscore_nbacom',
            'boxscore_cbssports',
            'playbyplay_espn',
            'playbyplay_nbacom',
            'shotchart_cbssports',
            'shotchart_espn',
            'shotchart_nbacom',
            'playbyplay_statsnbacom',
            'shotchart_statsnbacom',
            'boxscore_statsnbacom'
        ]

    # Choose games
    lgobj = league.League(dbobj, league_name)
    if not lgobj.obj or not lgobj.league_season:
        print "Could not find league. Quitting."
        return False
    else:
        print "+++ League identified: %s" % (str(lgobj.obj))
        print "+++ League season identified: %s" % (str(lgobj.league_season))
        games = lgobj.getGames(dt)
        files = lgobj.getModules()

        # Get source
        gamedata = source.main.go(games, files)

        # Scrape
        extract.main.go(gamedata)
        clean.main.go(gamedata, dbobj)
        load.main.go(gamedata, dbobj)


# League-specific methods

def run(league = '', league_id = 0, league_season_id = 0, start_date = 0, end_date = 0, date = 0):
    pass



def backfill(league = '', league_id = 0, league_season_id = 0, start_date = 0, end_date = 0, date = 0):
    pass


def main():

    files = []
    try:
        league_name = sys.argv[1]
        dt = sys.argv[2]
        dt = datetime.date(*map(int,dt.split('-')))

        if len(sys.argv) > 3:
            files = sys.argv[3:]
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)

    print dt
    scrapeAuto(league_name, dt, files)
    #obj = Scrape(league='nba')
    

if __name__ == '__main__':
    main()
