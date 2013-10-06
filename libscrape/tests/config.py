import unittest
from libscrape.config import constants
from libscrape.config import config



class ConfigSetup(unittest.TestCase):


    def testConstantsForLeaguesExist(self): 
        self.assertTrue('nba' in constants.URL)
        self.assertTrue('wnba' in constants.URL)


    def testConstantsForDataSourcesExistNba(self):
        league = 'nba'
        self.assertTrue('SHOTCHART_CBSSPORTS' in constants.URL[league])
        self.assertTrue('PLAYBYPLAY_NBACOM' in constants.URL[league])
        self.assertTrue('SHOTCHART_NBACOM' in constants.URL[league])
        self.assertTrue('PLAYBYPLAY_ESPN' in constants.URL[league])
        self.assertTrue('SHOTCHART_ESPN' in constants.URL[league])
        self.assertTrue('SHOTCHART_NBACOM' in constants.URL[league])


    def testConstantsForDataSourcesExistWnba(self):
        league = 'wnba'
        self.assertTrue('PLAYBYPLAY_NBACOM' in constants.URL[league])
        self.assertTrue('SHOTCHART_NBACOM' in constants.URL[league])
        self.assertTrue('PLAYBYPLAY_ESPN' in constants.URL[league])
        self.assertTrue('SHOTCHART_ESPN' in constants.URL[league])
        self.assertTrue('SHOTCHART_NBACOM' in constants.URL[league])


    def testConfigLeaguesExist(self):
        self.assertTrue('nba' in config.league)
        self.assertTrue('wnba' in config.league)



def main():
    unittest.main()


if __name__ == '__main__':
    main()
