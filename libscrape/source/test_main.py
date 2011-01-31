import unittest
import datetime
import main
from libscrape.config import constants
import os
import sys


class checkGames(unittest.TestCase):
    def testGamesExist(self):
        self.assertTrue(main.chooseGames('2010-10-27'))

    def testNoGamesReturnEmpty(self):
        self.assertFalse(main.chooseGames('2010-12-24'))
        

    def testSourceExtractReturnsCorrectNumberOfFiles(self):
        dt = datetime.date.today() - datetime.timedelta(days=1)
        games = main.chooseGames(dt)
        main.main(dt)
        game_files = [f for f in os.listdir(constants.LOGDIR_SOURCE) if f[:10] == dt.isoformat()]
        
        self.assertEqual(len(games) * 2,len(game_files)) 

if __name__ == '__main__':
    unittest.main()
