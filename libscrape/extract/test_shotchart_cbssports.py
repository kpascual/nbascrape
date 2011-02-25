import unittest
import os
from shotchart_cbssports import ShotExtract
from libscrape.config import db
from libscrape.config import constants
import MySQLdb


gamedata = []

LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

def sample():
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
    
def chooseRandomGames():
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("SELECT * FROM game WHERE date_played <= NOW() ORDER BY RAND() LIMIT 3")
    return curs.fetchall()

def findSourceGameFiles(game_name):
    return [itm for itm in os.listdir(constants.LOGDIR_SOURCE) if game_name in itm and 'shotchart_cbssports' in itm][0]



class CheckShots(unittest.TestCase):

    def setUp(self):
        self.gamedata = gamedata[0]
        self.filename = self.gamedata['filename']
        self.obj = ShotExtract(**self.gamedata)
        self.away_team = self.gamedata['away_team']
        self.home_team = self.gamedata['home_team']

    def testPlayerData(self):
        for itm in self.obj.getHomePlayers():
            self.assertEqual(len(itm),9)
        for itm in self.obj.getAwayPlayers():
            self.assertEqual(len(itm),9)


    def testCourtDimensions(self):
        self.assertEqual(self.obj.assertCourtDimensions(),(300, 282))

    def testShotDefinitions(self):
        shots = db.nba_query("SELECT * FROM cbsshot") 

        for line in self.obj.assertShotDefinitions():
            converted = (int(line[0]),line[1])
            self.assertTrue(converted in shots, "%s not found in known shots" % str(line))

    def testShotData(self):
        for row in self.obj.getShotData():
            self.assertEqual(len(row),10)
    
    def testAwayAndHomeTeams(self):
        self.assertTrue(self.obj.away_team,self.away_team)
        self.assertTrue(self.obj.home_team,self.home_team)
    
    def testExtract(self):
        self.obj.extractAndDump()
        self.assertTrue(self.filename + '_players' in os.listdir(LOGDIR_EXTRACT)) 
        self.assertTrue(self.filename + '_shots' in os.listdir(LOGDIR_EXTRACT)) 


if __name__ == '__main__':
    sample()
    unittest.main()
