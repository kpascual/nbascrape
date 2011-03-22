import urllib2
import re
import csv
import datetime
import sys
import logging
import logging.config
from BeautifulSoup import BeautifulSoup
from libscrape.config import constants

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("extract")

LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class ShotExtract:

    def __init__(self, html, game_name, filename, away_team, home_team):
        self.html = html
        self.game_name = game_name
        self.away_team = away_team
        self.home_team = home_team 
        self.filename = filename


    def extractAndDump(self):
        home_players = self.getHomePlayers() 
        away_players = self.getAwayPlayers() 
        shots = self.getShotData()
        self._dumpShots(shots)
        self._dumpPlayers(home_players + away_players)

    def getHomePlayers(self):
        pattern = re.compile(".*var\s+playerDataHomeString\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")
        
        match = pattern.search(self.html)
        if match:
            matched = [[self.home_team, player.split(':')[0]] + player.split(':')[1].split(',') for player in match.group('info').split('|')] 
            return matched

        logger.warn("No Home Players found in CBS Sports Shot Chart Data")
        return []


    def getAwayPlayers(self):
        pattern = re.compile(".*var\s+playerDataAwayString\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")
        
        match = pattern.search(self.html)
        if match:
            matched = [[self.away_team, player.split(':')[0]] + player.split(':')[1].split(',') for player in match.group('info').split('|')] 
            return matched

        logger.warn("No Away Players found in CBS Sports Shot Chart Data")
        return []


    def getShotData(self):
        pattern = re.compile(".*var\s+currentShotData\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")

        list_shotdata = []
        matches = pattern.search(self.html)
        if matches:
            shotdata = matches.group('info')
            list_shotdata = [[i] + itm.split(',') for i,itm in enumerate(shotdata.split('~'))]
        else:    
            logger.warn("No Shot data found in CBS Sports shot data")

        return list_shotdata


    def _dumpShots(self, data):
        writer = csv.writer(open(LOGDIR_EXTRACT + self.filename + '_shots','wb'),delimiter=',',lineterminator='\n')
        writer.writerows(data)


    def _dumpPlayers(self, data):
        writer = csv.writer(open(LOGDIR_EXTRACT + self.filename + '_players','wb'),delimiter=',',lineterminator='\n')
        writer.writerows(data)


    def assertCourtDimensions(self):
        x = 0
        y = 0

        matchx = re.search(".*sp\.x\s+=\s+(?P<x>\d+).*",self.html)
        matchy = re.search(".*sp\.y\s+=\s+(?P<y>\d+).*",self.html)
        
        if matchx:
            x = int(matchx.group('x'))
        if matchy:
            y = int(matchy.group('y'))

        return (x, y)

    
    def assertShotDefinitions(self):
        match = re.findall(".*sp\.shotTypeArray\[(?P<index>\d+)\]\s+=\s+\"(?P<name>[0-9a-zA-Z\s]+)\";.*",self.html)
        if match:
            return match

        return []



"""
def getShotData(strng):
    # Get shot data
    pattern= re.compile(".*var\s+currentShotData\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")

    shotdata = ''
    list_shotdata = []
    matches = pattern.search(strng)
    if matches:
        shotdata = matches.group('info')
        list_shotdata = shotdata.split('~')
        print shotdata 
    return list_shotdata


def getTeamAbbrev(strng):
    patternAway = re.compile(".*sp\.homeAbbr\s+\=\s+\"(?P<team>\w+)\".+")
    patternHome = re.compile(".*sp\.awayAbbr\s+\=\s+\"(?P<team>\w+)\".+")
    
    match_away = patternAway.search(strng)
    match_home = patternHome.search(strng)
    
    if match_away:
        away_team = match_away.group('team')
    
    if match_home:
        home_team = match_home.group('team')
    
    return ['0:%s;1:%s' % (home_team,away_team)]
        

def getPlayers(strng):
    list_playerdata = []

    patternHomePlayerData = re.compile(".*var\s+playerDataHomeString\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")
    patternAwayPlayerData = re.compile(".*var\s+playerDataAwayString\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")
    
    match_home = patternHomePlayerData.search(strng)
    match_away = patternAwayPlayerData.search(strng)
    
    for match in [match_home, match_away]:
        if match:
            matched = match.group('info')
            list_playerdata.append(matched)
            
    return list_playerdata 
    

def logToFile(list_data,str_filename):
    f = open(LOGDIR_EXTRACT + str_filename,'w')
    str_data = '\n'.join([str(itm) for itm in list_data])
    f.write(str_data)
    f.close()


def main(game_data):
    (away_team, home_team, dt, espn_game_id, cbssports_game_id) = game_data
    
    response = urllib2.urlopen("http://www.cbssports.com/nba/gametracker/shotchart/NBA_" + cbssports_game_id)
    str_doc = response.read()
   
    print "--- Parsing CBS Sports Shot Chart Data on %s" % cbssports_game_id

    # Get dict of player id and player metadata
    print "--- Getting player metadata ..."
    list_playerdata = getPlayers(str_doc)
    filename_players = '%s_cbssports_players' % cbssports_game_id
    logToFile(list_playerdata,filename_players)
    print "--- Successful!"
 
    # Get away team/home team abbreviations
    print "--- Getting team abbreviations ..."
    abbrev = getTeamAbbrev(str_doc)
    filename_teams = '%s_cbssports_teams' % cbssports_game_id
    logToFile(abbrev,filename_teams)
    print "--- Successful!"

    # Shot Data
    print "--- Getting shot data ..."
    list_shot_data = getShotData(str_doc)
    filename_shotchart = '%s_cbssports_shotchart' % cbssports_game_id
    logToFile(list_shot_data,filename_shotchart)
    print "--- Successful!"
    
    return [
        filename_players,
        filename_teams,
        filename_shotchart
    ]

if __name__ == '__main__':
    sys.exit(main('20101128_NY@DET'))
"""    
    
#shot data index of values, after split by ~
# 1: possession (0 == away team, 1 == home team)
# 2: miltime
# 3: current period
# 4: player_id
# 5: shot type (there's a map found in javascript)
# 6: shot result
# 7: x coordinate
# 8: y coordinate
# 9: distance

# player data index of values
# 1: player name (&nbsp; should be replaced with a space " ")
# 2: jersey #
# 3: position
# 4: FG data
# 5: 3pt data
# 6: free throw data
# 7: total points
# 8: totals

# Dimensions of court: 300 wide, 282 length, ratio? 6
