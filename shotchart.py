import urllib2
import re
import datetime
import sys
from BeautifulSoup import BeautifulSoup


dict_shot_type = {}
dict_shot_type[0] = "Shot"
dict_shot_type[1] = "Jump Shot"
dict_shot_type[2] = "Running Jump"
dict_shot_type[3] = "Hook Shot"
dict_shot_type[4] = "Tip-in"
dict_shot_type[5] = "Layup"
dict_shot_type[6] = "Driving Layup"
dict_shot_type[7] = "Dunk Shot"
dict_shot_type[8] = "Slam Dunk"
dict_shot_type[9] = "Driving Dunk"
dict_shot_type[10] = "Free Throw"
dict_shot_type[11] = "1st of 2 Free Throws"
dict_shot_type[12] = "2nd of 2 Free Throws"
dict_shot_type[13] = "1st of 3 Free Throws"
dict_shot_type[14] = "2nd of 3 Free Throws"
dict_shot_type[15] = "3rd of 3 Free Throws"
dict_shot_type[16] = "Technical Free Throw"
dict_shot_type[17] = "1st of 2 Free Throws"
dict_shot_type[18] = "2nd of 2 Free Throws"
dict_shot_type[19] = "Finger Roll"
dict_shot_type[20] = "Reverse Layup"
dict_shot_type[21] = "Turnaround Jump Shot"
dict_shot_type[22] = "Fadeaway Jump Shot"
dict_shot_type[23] = "Floating Jump Shot"
dict_shot_type[24] = "Leaning Jump Shot"
dict_shot_type[25] = "Mini Hook Shot"


def getShotData(strng):
    # Get shot data
    patternShotData = re.compile(".*var\s+currentShotData\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")

    shotdata = ''
    list_shotdata = []
    matches = patternShotData.search(strng)
    if matches:
        shotdata = matches.group('info')
        list_shotdata = shotdata.split('~')
        
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
    
    return {'0': home_team, '1': away_team}
        

def getPlayerMap(strng):
    list_keys = ['name','jersey','position','data_fg','data_3pt','data_ft','total_points']
    dict_players = {}

    patternHomePlayerData = re.compile(".*var\s+playerDataHomeString\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")
    patternAwayPlayerData = re.compile(".*var\s+playerDataAwayString\s+\=\s+new\s+String\(\"(?P<info>.+)\"\).+")
    
    match_home = patternHomePlayerData.search(strng)
    match_away = patternAwayPlayerData.search(strng)
    
    for match in [match_home, match_away]:
        if match:
            matched = match.group('info')
            data = matched.split('|')
            for itm in data:
                (player_id,player_info) = itm.split(':')
                #print player_info
                d = dict(zip(list_keys,player_info.split(',')))
                dict_players[player_id] = d
    #print dict_players

    return dict_players
    


def cleanData(list_shotdata):
    return_data = []
    last_seconds = 721
    last_period = 1
    adj_period = 1
    
    for itm in list_shotdata:
    
        # convert all times to seconds
        (possession,time_left,period,player_id,shot_type,shot_result,x,y,distance) = itm.split(',')
        seconds_convert = time_left.split(':')
        if len(seconds_convert) > 1:
            new_seconds = int(seconds_convert[0]) * 60 + int(seconds_convert[1])
        else:        
            new_seconds = int(seconds_convert[0].split('.')[0])
            
        # Quarter 4 is mis-labeled on CBS sports, so convert mis-labeled quarter 3's to quarter 4
        if last_seconds < new_seconds and last_period == '3':
            adj_period = 4
            print "change period"
        elif last_seconds < new_seconds and int(last_period) >= 4:
            adj_period = int(last_period) + 1
        
        if adj_period != 4:
            adj_period = int(period)
            
        #print ','.join([str(period),str(adj_period),str(new_seconds),str(last_period),str(last_seconds)])
        return_data.append((possession,new_seconds,adj_period,player_id,dict_shot_type[int(shot_type)],shot_result,x,y,distance)) 
        
        last_period = period
        last_seconds = new_seconds
    
    return return_data




def parse_game(str_cbs_sports_game_id):
    response = urllib2.urlopen("http://www.cbssports.com/nba/gametracker/shotchart/NBA_" + str_cbs_sports_game_id)
    str_strings = response.read()
    
    # Get dict of player id and player metadata
    player_map = getPlayerMap(str_strings)
    
    # Get away team/home team abbreviations
    abbrev = getTeamAbbrev(str_strings)


    # Shot Data
    clean_data = cleanData(getShotData(str_strings))
    clean2 = []
    for (possession,new_seconds,adj_period,player_id,shot_type,shot_result,x,y,distance) in clean_data:
        
        new = (abbrev[possession],new_seconds,adj_period,player_map[player_id]['name'],shot_type,shot_result,25+int(x), \
                47-abs(int(y)),distance)
        
        clean2.append(new)

    #print len(clean2)

    print '\n'.join([','.join([str(field) for field in itm]) for itm in clean2])
    
    #print player_map
    # Print results
    #for itm in clean_data:
        #print itm
    

if __name__ == '__main__':
    sys.exit(parse_game('20101128_NY@DET'))
    
    
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