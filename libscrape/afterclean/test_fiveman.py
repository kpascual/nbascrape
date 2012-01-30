import fiveman
from libscrape.config import db
import unittest

    
sample = db.nba_query_dict("SELECT * FROM game WHERE date_played <= '2011-02-20' ORDER BY RAND() LIMIT 10")
#sample = db.nba_query_dict("SELECT * FROM game WHERE id = 666")


class CheckFiveMan(unittest.TestCase):
    def setUp(self):
        self.objs = [fiveman.FiveMan(game['id'],game['away_team'],game['home_team'], game['date_played']) for game in sample]


    def testAllPlaysHaveFiveHomePlayers(self):
        for obj in self.objs:
            #print '%s vs %s' % (obj.away_team, obj.home_team)
            result = obj.getHomeFiveManUnit()

            print "game_id: %s, %s vs %s" % (obj.game_id, obj.away_team, obj.home_team)
            for period in result:
                for line in period:
                    
                    self.assertTrue(len(line[2]) <= 5, "play has greater than 5 players: play num: %s" % line[0])


    def testAllPlaysHaveFiveAwayPlayers(self):
        for obj in self.objs:
            result = obj.getAwayFiveManUnit()

            print "game_id: %s, %s vs %s" % (obj.game_id, obj.away_team, obj.home_team)

            for period in result:
                for line in period:
                    #print line
                    self.assertTrue(len(line[2]) <= 5, "play has greater than 5 players: play num: %s" % line[0])


    def testGo(self):
        for obj in self.objs:
            result = obj.go()

if __name__ == '__main__':
    unittest.main()
