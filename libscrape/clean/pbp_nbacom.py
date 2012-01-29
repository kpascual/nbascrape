import re
import datetime
import csv
from BeautifulSoup import BeautifulStoneSoup

from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class Clean:

    def __init__(self, xml, dbobj):
        self.xml = xml
        self.qry = qryobj


    def getPlayByPlayData(self):
        soup = BeautifulStoneSoup(self.xml)
        playbyplaydata = soup.findAll("event")
        for play in playbyplaydata:
            playdata = dict(play.attrs)
            playdata['text'] = play.contents[0]
            playdata['time_left'] = self._transformTimeToTenthSeconds(playdata['game_clock'])
            print playdata


    def _transformTimeToTenthSeconds(self, game_clock):

        mins, secs = game_clock.split(':')
        total_secs = int(mins)*60*10 + int(float(secs) * 10)

        return total_secs


    def resolvePlayer(self, player_code):
        pass

    
    def _resolveTeam(self, nbacom_team_code):
        team = self.qry.query("SELECT * FROM team WHERE nbacom_code = '%s'" % (nbacom_team_code))
        return team[0][0]


    def _getExistingPlayerId(self, player_code):
        pass


def main():
    f = '2011-12-17_SAC@GS_pbp_nbacom'
    obj = Clean(open('../../logs/source/' + f,'r').read())
    
    print obj.getPlayByPlayData()


if __name__ == '__main__':
    main()
