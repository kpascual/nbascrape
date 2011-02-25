import random
import MySQLdb
import datetime
import unittest
import os

from libscrape.config import constants
from libscrape.config import db
import pbp_espn
import test_pbp_espn_data


gamedata = []


def chooseGames(date_played):
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("SELECT * FROM game WHERE date_played = '%s'" % (date_played))
    return curs.fetchall()

def chooseRandomGames():
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("SELECT * FROM game WHERE date_played <= NOW() ORDER BY RAND() LIMIT 3")
    return curs.fetchall()

def findSourceGameFiles(game_name):
    return [itm for itm in os.listdir(constants.LOGDIR_SOURCE) if game_name in itm and 'pbp_espn' in itm][0]

def test_sample():
    global gamedata

    games = chooseRandomGames()
    for g in games:
        try:
            sourcehtml = open(constants.LOGDIR_SOURCE + findSourceGameFiles(g['abbrev']),'r').read()
            game = {
                'home_team': g['home_team'],
                'away_team': g['away_team'],
                'game_name': g['abbrev'],
                'html': sourcehtml,
                'filename': g['abbrev']
            }
            gamedata.append(game)
        except:
            print "+++ Could not find source doc for %s" % g['abbrev']

    
def test_yesterday():
    global gamedata

    dt = datetime.date.today() - datetime.timedelta(days=1)
    games = chooseGames(dt)

    for g in games:
        try:
            sourcehtml = open(LOGDIR_SOURCE + findSourceGameFiles(g['abbrev']),'r').read()
            game = {
                'home_team': g['home_team'],
                'away_team': g['away_team'],
                'game_name': g['abbrev'],
                'html': sourcehtml
            }
            gamedata.append(game)
        except:
            print "+++ Could not find source doc for %s" % g['abbrev']



class CheckDataLooksNormal(unittest.TestCase):
    def setUp(self):
        self.gamedata = gamedata
        self.extract = [pbp_espn.Extract(**g) for g in self.gamedata]

    
    def testRowLengths(self):
        for e in self.extract:
            self.assertEqual(sorted([r[0] for r in e.examineRowLengths()]),[0,1,2,4])


    def testPeriodsDontOverlap(self):
        for e in self.extract:
            indexes = [index for (index, quarter) in e.getPeriodRanges()]
            self.assertEqual(max([indexes.count(itm) for itm in indexes]),1)


    def testRowHeadersHaveOnlyTwoTeams(self):
        possible_items = ['SCORE','TIME']
        possible_items.extend(constants.LIST_TEAMS)
        for e in self.extract:
            (home, away) = e.getTeamNames()
            self.assertTrue(home in possible_items)
            self.assertTrue(away in possible_items)


    def testPeriodRanges(self):
        for e in self.extract:
            periods = e.getPeriodRanges()
            for indexes in periods:
                self.assertEqual(len(indexes),2)


    def testTimeouts(self):
        for e in self.extract:
            e.getTimeouts()

    def testPlayData(self):
        for e in self.extract:
            self.assertTrue(e.getPlayData())

    def testBackupPeriod(self):
        for e in self.extract:
            pass

    #def testExtractAll(self):
    #    for e in self.extract:
    #        e.extractAll()

    def testBackupPeriods(self):
        for e in self.extract:
            print e.getPeriodIndexes()

if __name__ == '__main__':
    test_sample()
    unittest.main()
