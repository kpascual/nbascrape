import pbp_espn
import test_pbp_espn_data
import unittest
import os
from libscrape.config import constants
import random

"""
class checkParse(unittest.TestCase):
    def setUp(self):
        games = [f for f in os.listdir(constants.LOGDIR_SOURCE) if int(f[:10].replace('-','')) % 3 == 0 and 'espn' in f]
        self.sample = random.sample(games,4)


    def testPbpOnlyHasZeroTwoOrFourItems(self):
        #parseData() 
        list_cells = [cells for g in self.sample for cells in test_pbp_espn_data.testParseTableLengths(open(constants.LOGDIR_SOURCE + g,'r').read())]
        summary = set([(a,list_cells.count(a)) for a in list_cells])

        self.assertEqual(sorted([int(a[0]) for a in summary]),[0,1,2,4])
"""

class CheckDataLooksNormal(unittest.TestCase):
    def setUp(self):
        self.games = [f for f in os.listdir(constants.LOGDIR_SOURCE) if int(f[:10].replace('-','')) % 3 == 0 and 'espn' in f]
        self.sample = random.sample(self.games,1)
        self.extract = [pbp_espn.Extract(open(constants.LOGDIR_SOURCE + s,'r').read()) for s in self.sample]
        print self.sample        

    
    def testRowLengths(self):
        for e in self.extract:
            self.assertEqual(sorted([r[0] for r in e.examineRowLengths()]),[0,1,2,4])


    def testQuartersDontOverlap(self):
        for e in self.extract:
            indexes = [index for (index, quarter) in e.getPeriodRanges()]
            self.assertEqual(max([indexes.count(itm) for itm in indexes]),1)


    def testZeroItemRowsAreHeaders(self):
        possible_items = ['SCORE','TIME']
        possible_items.extend(constants.LIST_TEAMS)
        for e in self.extract:
            self.assertTrue(e.examineZeroCells())


    def testRowHeadersHaveOnlyTwoTeams(self):
        possible_items = ['SCORE','TIME']
        possible_items.extend(constants.LIST_TEAMS)
        for e in self.extract:
            (home, away) = e.getTeamNames()
            self.assertTrue(home in possible_items)
            self.assertTrue(away in possible_items)


    def testValuesForOneItemTableRows(self):
        for e in self.extract:
            rows = e.examineOneCell()
            for row in rows:
                self.assertTrue('Quarter Summary' in row[0] or 'Overtime Summary' in row[0], 'This was found instead: %s' % str(row[0]))


    def testPeriodIndexes(self):
        for e in self.extract:
            periods = e.getPeriodIndexes()
            for p, indexes in periods.items():
                self.assertEqual(len(indexes),2)


    def testTimeouts(self):
        for e in self.extract:
            e.getTimeouts()

    def testPlayData(self):
        for e in self.extract:
            self.assertTrue(e.getPlayData())

    def testExtractAll(self):
        for e in self.extract:
            e.extractAll()
    

if __name__ == '__main__':
    unittest.main()
