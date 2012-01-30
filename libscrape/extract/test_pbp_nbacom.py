import random
import MySQLdb
import datetime
import unittest
import os

from libscrape.config import constants
from libscrape.config import db
import pbp_nbacom

gamedata = []


def chooseGames():
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("SELECT * FROM game WHERE date_played between '2010-10-24' and '2011-02-25'")
    return curs.fetchall()


def getGameDictionaries():

    games = chooseGames()
    game_metadata = []
    for g in games:
        try:
            filename = '%s_pbp_nbacom' % (g['abbrev'])
            sourcehtml = open(constants.LOGDIR_SOURCE + filename,'r').read()
            game = {
                'home_team': g['home_team'],
                'away_team': g['away_team'],
                'game_name': g['abbrev'],
                'html': sourcehtml,
                'filename': g['abbrev']
            }
            game_metadata.append(game)
        except:
            print "+++ Could not find source doc for %s" % g['abbrev']

    return game_metadata


class CheckDataLooksNormal(unittest.TestCase):
    def setUp(self):
        self.objs = (pbp_nbacom.Extract(**game) for game in getGameDictionaries())


    """
    def testExtract(self):
        for obj in self.objs:
            print obj.game_name
            obj.extract() 

    def testPeriodIndexesHaveOneStartAndEnd(self):
        for obj in self.objs:
            indexes = obj.getPeriodIndexes() 
            print obj.game_name

            for period in indexes:
                self.assertTrue(len(period) == 3,indexes)
    """

    def testExtract(self):
        for obj in self.objs:
            print obj.game_name
            obj.extract()


if __name__ == '__main__':
    unittest.main()
