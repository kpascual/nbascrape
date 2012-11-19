from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime
from libscrape.config import db
import time


# A script that scrapes ESPN.com's scoreboard to retrieve ESPN's game_id and store into MySQL db
dbobj = db.Db(db.dbconn_nba)

def getScoreboardDoc(dt): 
    url = 'http://espn.go.com/nba/scoreboard?date=%s' % dt.isoformat().replace('-','')
    response = urllib2.urlopen(url)
    return response.read()


def getGameIdsAndTeams(html):
    soup = BeautifulSoup(html)
    links = soup.findAll(href=re.compile("/nba/conversation.*"))
    links = list(set(links))

    game_ids = []
    for l in links:
        match = re.search("/nba/conversation\?gameId=(?P<game_id>[0-9]+)$",l['href'])
        
        if match:
            found = match.groupdict()
            game_ids.append(found['game_id'])

    game_info = []
    for game_id in game_ids:
        
        try:
            team_div = soup.findAll(id='%s-aTeamName' % game_id)
            away_team_id, away_team, away_team_nbacom, away_team_nickname = findTeamName(team_div[0].a.renderContents())

            team_div = soup.findAll(id='%s-hTeamName' % game_id)
            home_team_id, home_team, home_team_nbacom, home_team_nickname = findTeamName(team_div[0].a.renderContents())

            game_info.append(
                {'espn_game_id':game_id, 'away_team': away_team, 
                'home_team': home_team, 'away_team_nbacom': away_team_nbacom, 'home_team_nbacom': home_team_nbacom,
                'away_team_id': away_team_id, 'home_team_id': home_team_id, 
                'away_team_nickname': away_team_nickname, 'home_team_nickname': home_team_nickname
                }
            )
        except:
            print "Could not find teams.  Skipping this game: %s" % (game_id)



    return game_info


def findTeamName(name):
    team_data = _getTeamData()
    
    for team in team_data:
        if name == team['nickname'] or name == team['alternate_nickname']:
            return (team['id'], team['code'],team['nbacom_code'], team['nickname'])
        else:
            pass

    return (0,0) 


def _getTeamData():
    result = dbobj.query_dict("SELECT * FROM team WHERE is_active = 1") 
    return result 


def _fillInGameData(current_season, season_type, game_data, dt):

    final = []
    for g in game_data:
        g['date_played'] = dt
        g['abbrev'] = '%s_%s@%s' % (dt, g['away_team'], g['home_team'])
        g['away_team_code'] = g['away_team']
        g['home_team_code'] = g['home_team']
        g['nbacom_game_id'] = '%s/%s%s' % (dt.isoformat().replace('-',''), g['away_team_nbacom'], g['home_team_nbacom'])
        g['cbssports_game_id'] = g['abbrev'].replace('-','')
        g['permalink'] = g['away_team_nickname'] + '-at-' + g['home_team_nickname'] + '-' + dt.strftime("%B-%d-%Y")
        g['permalink'] = g['permalink'].replace('-0','-').lower()
        g['season'] = current_season
        g['season_type'] = season_type
        final.append(g)

        del g['away_team_nickname']
        del g['home_team_nickname']
        del g['away_team_nbacom']
        del g['home_team_nbacom']

    return final


def _writeToDatabase(game, date_played):
    curs = dbobj.curs()

    sql = """
        INSERT IGNORE INTO game_temp (%s) VALUES (%s)
    """ % (','.join([field for field,val in sorted(game.items())]),','.join(["'%s'" % val for field,val in sorted(game.items())]))
    
    curs.execute(sql)

    # Get the game id -- on ignore, lastrowid won't return a value
    curs.execute("""
        SELECT id
        FROM game
        WHERE date_played = '%s' AND home_team_id = %s AND away_team_id = %s
    """ % (game['date_played'], game['home_team_id'], game['away_team_id']))
    game_id = curs.fetchone()
    #print game_id


    if game['season_type'] == 'POST':
        curs.execute("""
            SELECT id 
            FROM
                playoff_series
            WHERE
                season = '%s'
                AND (team1_id = '%s' AND team2_id = '%s')
                OR (team1_id = '%s' AND team2_id = '%s')
        """ % (game['season'], game['home_team_id'], game['away_team_id'], game['away_team_id'], game['home_team_id']))
        playoff_series = curs.fetchone()
        print playoff_series

        if playoff_series:
            sql = """
                INSERT INTO rel_playoff_game (game_id, playoff_series_id) VALUES (%s, %s)
            """ % (game_id[0], playoff_series[0])
            curs.execute(sql)
            print sql



def fillInAllDates():

    start_dt = datetime.date(2012,10,30)
    end_dt = datetime.date(2012,11,4)
    dt = start_dt

    while dt < end_dt:

        #print dt
        go(dt)

        dt = dt + datetime.timedelta(days=1)
    


def go(dt):
    current_season = '2012-2013'
    season_type = 'REG'
    
    html = getScoreboardDoc(dt)
    gamedata = getGameIdsAndTeams(html)
    complete_gamedata = _fillInGameData(current_season, season_type, gamedata, dt)

    for game in complete_gamedata:
        print game
        dbobj.insert_or_update('game_temp',[game])
        #_writeToDatabase(game, dt)
    



if __name__ == '__main__':
    fillInAllDates()
