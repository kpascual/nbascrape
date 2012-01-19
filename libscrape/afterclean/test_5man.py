import fiveman
from libscrape.config import db
import unittest

    
sample = db.nba_query_dict("SELECT * FROM game WHERE date_played <= '2011-02-26' ORDER BY RAND() LIMIT 10")
#sample = db.nba_query_dict("SELECT * FROM game WHERE id = 240")


class CheckFiveMan(unittest.TestCase):
    def setUp(self):
        self.objs = [fiveman.FiveMan(game['id'],game['away_team'],game['home_team'], game['date_played']) for game in sample]


    def testAllPlaysHaveFiveHomePlayers(self):
        for obj in self.objs:
            result = obj.getHomeFiveManUnit()

            print "game_id: %s" % obj.game_id
            for period in result:
                for line in period:
                    #print line
                    self.assertEqual(len(line[2]),5)


    def testAllPlaysHaveFiveAwayPlayers(self):
        for obj in self.objs:
            result = obj.getAwayFiveManUnit()

            print "game_id: %s" % obj.game_id

            for period in result:
                for line in period:
                    #print line
                    self.assertEqual(len(line[2]),5)


if __name__ == '__main__':
    unittest.main()
