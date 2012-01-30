from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime
from libscrape.config import db


# A script that scrapes ESPN.com's scoreboard to retrieve ESPN's game_id and store into MySQL db


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
        away_team = findTeamName(team_div[0].a.renderContents())

        team_div = soup.findAll(id='%s-homeTeamName' % game_id)
        home_team = findTeamName(team_div[0].a.renderContents())

        game_info.append({'espn_game_id':game_id, 'away_team': away_team, 'home_team': home_team})

    return game_info


def findTeamName(name):
    team_data = _getTeamData()
    
    for team in team_data:
        if name == team['nickname'] or name == team['alternate_nickname']:
            return team['code']
        else:
            pass

    return 0 


def _getTeamData():
    result = db.nba_query_dict("SELECT * FROM team") 
    return result 


def _fillInGameData(game_data, dt):
    final = []
    for g in game_data:
        g['date_played'] = dt
        g['abbrev'] = '%s_%s@%s' % (dt, g['away_team'], g['home_team'])
        g['cbssports_game_id'] = g['abbrev'].replace('-','')
        final.append(g)

    return final


def _writeToDatabase(games, date_played):
    for g in games:
        sql = """
            INSERT IGNORE INTO game (%s) VALUES (%s)
        """ % (','.join([field for field,val in sorted(g.items())]),','.join(["'%s'" % val for field,val in sorted(g.items())]))
        
        db.nba_query(sql)

        sql_update_nbacom = """
            UPDATE game g
                INNER JOIN team home_team ON home_team.code = g.home_team 
                INNER JOIN team away_team ON away_team.code = g.away_team 
            SET nbacom_game_id = CONCAT(replace(g.date_played,'-',''),'/',away_team.nbacom_code, home_team.nbacom_code) 
            WHERE g.date_played = '%s'   
        """ % date_played
        db.nba_query(sql_update_nbacom)


def fillInAllDates():
    current_date = datetime.date(2012,2,27)

    last_date = datetime.date(2012,4,26)

    while current_date <= last_date:
        print current_date
        main(current_date)

        current_date = current_date + datetime.timedelta(days=1)


def main(dt):
    
    html = getScoreboardDoc(dt)
    gamedata = getGameIdsAndTeams(html)
    complete_gamedata = _fillInGameData(gamedata, dt)

    _writeToDatabase(complete_gamedata, dt)


if __name__ == '__main__':
    fillInAllDates()
