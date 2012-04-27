from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime
from libscrape.config import db


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
        team_div = soup.findAll(id='%s-awayTeamName' % game_id)
        away_team_id, away_team, away_team_nbacom, away_team_nickname = findTeamName(team_div[0].a.renderContents())

        team_div = soup.findAll(id='%s-homeTeamName' % game_id)
        home_team_id, home_team, home_team_nbacom, home_team_nickname = findTeamName(team_div[0].a.renderContents())

        game_info.append(
            {'espn_game_id':game_id, 'away_team': away_team, 
            'home_team': home_team, 'away_team_nbacom': away_team_nbacom, 'home_team_nbacom': home_team_nbacom,
            'away_team_id': away_team_id, 'home_team_id': home_team_id, 
            'away_team_nickname': away_team_nickname, 'home_team_nickname': home_team_nickname
            }
        )

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
    result = dbobj.query_dict("SELECT * FROM team") 
    return result 


def _fillInGameData(game_data, dt):
    CURRENT_SEASON = '2011-2012'
    SEASON_TYPE = 'POST'

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
        g['season'] = CURRENT_SEASON
        g['season_type'] = SEASON_TYPE
        final.append(g)

        del g['away_team_nickname']
        del g['home_team_nickname']
        del g['away_team_nbacom']
        del g['home_team_nbacom']

    return final


def _writeToDatabase(games, date_played):
    for g in games:
        sql = """
            INSERT IGNORE INTO game (%s) VALUES (%s)
        """ % (','.join([field for field,val in sorted(g.items())]),','.join(["'%s'" % val for field,val in sorted(g.items())]))
        
        dbobj.query(sql)



def fillInAllDates():
    dt = datetime.date(2012,4,28)

    print dt
    main(dt)



def main(dt):
    
    html = getScoreboardDoc(dt)
    gamedata = getGameIdsAndTeams(html)
    complete_gamedata = _fillInGameData(gamedata, dt)

    _writeToDatabase(complete_gamedata, dt)


if __name__ == '__main__':
    fillInAllDates()
