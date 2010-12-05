import urllib2
import re
import datetime
import sys
from BeautifulSoup import BeautifulSoup


def playbyplay(str_html):

    list_plays = []
    list_recognized_plays = []
    
    
    current_quarter = 1
    
    soup = BeautifulSoup(str_html)
    tables = soup.find(attrs={'class':'mod-data'})
    tr = tables.findAll('tr')
    
    print "START SCRAPING PLAY BY PLAY DATA"
    
    for itm in tr:
        td = itm.findAll('td')
        time_left = 0
        # Headers for tables
        if len(td) == 0:
            th = itm.findAll('th')
            away = th[1].renderContents()
            home = th[3].renderContents()
        # Start/end of quarters, full timeouts
        elif len(td) == 2:
            tuple_time_left = td[0].renderContents().split(':')
            time_left = int(tuple_time_left[0]) * 60 + int(tuple_time_left[1])
            
            match_quarter = re.search('.+Start\s+of\s+the\s+(?P<quarter>[0-9])(?P<abbrev>[a-zA-Z][a-zA-Z])\s+Quarter.+',str(td[1]))
            if match_quarter:
                # Obtain current quarter
                current_quarter = match_quarter.group('quarter')
                #print current_quarter
            
            # Check if this is a timeout
            txt = td[1].b.renderContents()
            match_timeout = re.search('(?P<team>[\w\s]+)\s+(?P<type>(full|20\s+Sec\.))\s+timeout',txt)
            if match_timeout:
                #print match_timeout.groupdict()
                d = 1
        elif len(td) == 4:
            tuple_time_left = td[0].renderContents().split(':')
            time_left = int(tuple_time_left[0]) * 60 + int(tuple_time_left[1])
            
            str_action = td[1].renderContents()
            
            find_play = choosePlayType(str_action)
            if len(find_play) > 0:
                list_recognized_plays.extend(find_play)
                
            match_action = re.findall('([A-Z]{1}[(a-z|A-Z).\']+)',str_action)
            if match_action:
                for nm in match_action:
                    str_action = str_action.replace(nm,'')
                if len(find_play) == 0:
                    list_plays.append(str_action)
                
        
    frq = [(a,list_plays.count(a)) for a in list_plays]
    for b in sorted(set(frq)):
        print ','.join([str(field) for field in b])
        #print str(current_quarter) + "-" + str(time_left)
    
    #for b in list_recognized_plays:
        #print b
    
    #print away
    #print home    


def choosePlayType(str_action):
    list_re = ['(<b>)*\s*(?P<off_player>[a-zA-Z.\'\s]+)\s+(?P<shot_result>(misses|makes))\s+(?P<length>[0-9]{1,2})-foot\s+(?P<shot_type>(jumper|three\s+point\s+jumper|two\s+point\s+shot))(</b>)*']

    list_matches = []
    for itm in list_re:
        match = re.search(itm,str_action)
        if match:
            #print match.groupdict()
            list_matches.append(match.groupdict())

    return list_matches




def parse_game(str_espn_game_id):
    response = urllib2.urlopen("http://espn.go.com/nba/playbyplay?gameId=" + str(str_espn_game_id) + "&period=0")
    str_strings = response.read()
    
    playbyplay(str_strings)
    

if __name__ == '__main__':
    sys.exit(parse_game('301121028'))
    
    
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