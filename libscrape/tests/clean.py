import unittest
from libscrape.config import constants
from libscrape.config import config
from libscrape.config import db

from libscrape.clean import pbp_espn
from libscrape.clean import pbp_nbacom


class PlayByPlayEspn(unittest.TestCase):

    def setUp(self):
        self.game_id = 1
        self.pbp_espn = pbp_espn.Clean('fake_filename',{'away_team_id':1,'home_team_id':2,'abbrev':'game','id':self.game_id,'date_played':'2013-01-01'},db.Db(config.dbconn_prod_nba))

    def test1(self):
        self.assertEqual(1,1)


    def testBlankScoreReplacement(self):
        plays = [
            {'away_score':1,'home_score':2},
            {'away_score':'','home_score':''}
        ]

        replaced = self.pbp_espn.replaceBlankScores(plays)
        self.assertEqual(replaced[1]['away_score'], 1)
        self.assertEqual(replaced[1]['home_score'], 2)


    def testBlankScoreFirstPlay(self):
        plays = [
            {'away_score':'','home_score':''},
            {'away_score':0,'home_score':2}
        ]

        replaced = self.pbp_espn.replaceBlankScores(plays)
        self.assertEqual(replaced[0]['away_score'], 0)
        self.assertEqual(replaced[0]['home_score'], 0)


    def testGameIdAdded(self):
        data = self.pbp_espn.addGameId([{}])
        self.assertTrue('game_id' in data[0])
        self.assertEqual(data[0]['game_id'], self.game_id)


    def testRequiredFieldsAdded(self):
        data = self.pbp_espn.fillInEmptyFields([{}])

        self.assertTrue('player_id' in data[0])
        self.assertEqual(data[0]['player_id'], -1)
        self.assertTrue('assist_player_id' in data[0])
        self.assertEqual(data[0]['assist_player_id'], -1)
        self.assertTrue('player1_id' in data[0])
        self.assertEqual(data[0]['player1_id'], -1)
        self.assertTrue('player2_id' in data[0])
        self.assertEqual(data[0]['player2_id'], -1)


    def testConformedTime(self):
        data = self.pbp_espn.replaceWithConformedTime([
            {'time_left': '3:45'},    
            {'time_left': '0:45'},    
        ])
        self.assertTrue('deciseconds_left' in data[0])
        self.assertTrue('time_left' not in data[0])
        self.assertEqual(data[1]['deciseconds_left'], 450)


    def testUnknownQuarter(self):
        data = self.pbp_espn.guessUnknownQuarters([
            {'period':1},
            {'period':'check quarter'},
        ])

        self.assertEqual(data[1]['period'], 1)


    def testPlayIdentification(self):
        plays = [
            "Lebron James blocks Kevin Garnett 's 22- foot jumper",
            "Lebron James misses 26- foot three point jumper",
            "<b>Lebron James makes three point jumper (Dwyane Wade assists )</b>",
            "<b>Lebron James makes two point shot (Dwyane Wade assists )</b>",
            "Lebron James travelling",
            "Lebron James offensive goaltending turnover",
            "Lebron James offensive Charge (Kevin Garnett draws the foul)",
            "Lebron James defensive 3-seconds (Technical Foul)",
            "Lebron James shooting foul (Kevin Garnett draws the foul)",
            #"Lebron James technical foul(1st technical foul)",
            "Lebron James  palming turnover",
            "Lebron James backcourt",
            "Lebron James lost ball turnover",
            "Lebron James  double dribble turnover",
            "Lebron James 5 second",
        ]

        for play in plays:
            play_espn_id, othervars = self.pbp_espn._findPlay(play)
            self.assertTrue(play_espn_id > 0, play)
            self.assertTrue(othervars['player_id'] > 0, play)


    def testPlaysWithTeam(self):
        plays = [
            '<b>Rockets 20 Sec. timeout</b>',
            '<b>Hornets Full timeout</b>',
        ]

        for play in plays:
            play_espn_id, othervars = self.pbp_espn._findPlay(play)
            self.assertTrue(play_espn_id in (109,110))
            self.assertTrue('team_id' in othervars.keys())


    def testPlaysWithPlayer2(self):
        plays = [
            "Lebron James lost ball turnover (Kevin Garnett steals)",
            "Lebron James vs. Kevin Garnett (Dwyane Wade gains possession)",
            "Lebron James offensive Charge (Kevin Garnett draws the foul)",
        ]

        for play in plays:
            play_espn_id, othervars = self.pbp_espn._findPlay(play)
            self.assertTrue('player2_id' in othervars.keys(),str(play_espn_id)+play)
            self.assertTrue('player_id' in othervars.keys())


class PlayByPlayNbacom(unittest.TestCase):


    def setUp(self):
        self.game_id = 1
        self.pbp_nbacom = pbp_nbacom.Clean('fake_filename',{'away_team_id':1,'home_team_id':2,'abbrev':'game','id':self.game_id,'date_played':'2013-01-01'},db.Db(config.dbconn_prod_nba))


    def testDeciseconds(self):
        deciseconds = self.pbp_nbacom._transformTimeToTenthSeconds('3:45')
        self.assertEqual(deciseconds, 2250)



def main():
    unittest.main()


if __name__ == '__main__':
    main()
