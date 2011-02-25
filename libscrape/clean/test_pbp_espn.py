import random
import unittest
import os

import pbp_espn


LOGDIR_EXTRACT = '../../logs/extract/'

games = [f for f in os.listdir(LOGDIR_EXTRACT) if int(f[:10].replace('-','')) % 3 == 0 and 'espn' in f]
sample = random.sample(games,1)
sample = ['2010-12-01_OKC@NJ_pbp_espn']

class CheckCleaning(unittest.TestCase):
    def setUp(self):
        self.games = games
        self.sample = sample

        #self.filename = LOGDIR_EXTRACT + '2011-01-30_MIA@OKC_pbp_espn'
        ##self.cleanobj = pbp_espn.Clean(self.filename)
        self.cleanobjs = [pbp_espn.Clean(f) for f in self.sample]


    def testUnknownQuartersHaveNoMoreChecks(self):
        for c in self.cleanobjs:
            cleaned = c.guessUnknownQuarters(c.plays)        
            checkquarter = [itm[0] for itm in cleaned if itm[0] == 'check quarter'] 
            self.assertEqual(len(checkquarter),0)


    def testBlankScoresAreCleaned(self):
        for c in self.cleanobjs:
            cleaned = c.replaceBlankScores(c.plays)
            all_scores = [itm[3] for itm in cleaned] + [itm[4] for itm in cleaned]
            self.assertTrue('' not in all_scores)


    def testAllPlaysHaveBeenIdentified(self):
        for c in self.cleanobjs:
            result = c.identifyPlays(c.plays)
            print c.filename
            self.assertTrue(0 not in [itm[5] for itm in result],'Sorry, found %s unknown plays' % result.count(0))

    def testCleanAll(self):
        for c in self.cleanobjs:
            c.cleanAll()

    def testAllPlaysHaveFiveManHomeUnits(self):
        pass

    def testAllPlaysHaveFiveManAwayUnits(self):
        pass

if __name__ == '__main__':
    unittest.main()


