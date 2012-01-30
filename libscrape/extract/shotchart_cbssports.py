import urllib2
import re
import csv
import datetime
import sys
from BeautifulSoup import BeautifulSoup
from libscrape.config import constants


LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class ShotExtract:

    def __init__(self, html, filename, gamedata):
        self.html = html
        self.gamedata = gamedata
        self.game_name = self.gamedata['abbrev']
        self.away_team = self.gamedata['away_team_id']
        self.home_team = self.gamedata['home_team_id']
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

        return []


    def getAwayPlayers(self):
        pattern = re.compile(".*var\s+playerDataAwayString\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")
        
        match = pattern.search(self.html)
        if match:
            matched = [[self.away_team, player.split(':')[0]] + player.split(':')[1].split(',') for player in match.group('info').split('|')] 
            return matched

        return []


    def getShotData(self):
        pattern = re.compile(".*var\s+currentShotData\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")

        list_shotdata = []
        matches = pattern.search(self.html)
        if matches:
            shotdata = matches.group('info')
            list_shotdata = [[i] + itm.split(',') for i,itm in enumerate(shotdata.split('~'))]
        else:    
            pass

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
