import shotchart_cbssports
import unittest


class CheckShotClean(unittest.TestCase):

    def setUp(self):
        self.filename = '2010-12-29_MEM@SAC_shotchart_cbssports'
        self.obj = shotchart_cbssports.CleanShots(self.filename)

    def testFoundExistingPlayers(self):
        self.assertTrue(self.obj.existing_players)

    def testIdentifyPlayer(self):
        self.assertTrue(self.obj.identifyPlayers())

    def testAllPlayersInShotDataAreIdentified(self):
        pass
    
    def testAdjustData(self):
        self.obj.adjustFourthPeriod(self.obj.shots)

    def testClean(self):
        self.obj.clean()

if __name__ == '__main__':
    unittest.main()
