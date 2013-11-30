from bs4 import BeautifulSoup
import urllib2
import re
import datetime
from libscrape.config import db
from libscrape.config import config
import time
import json


# A script that scrapes ESPN.com's scoreboard to retrieve ESPN's game_id and store into MySQL db
dbobj = db.Db(config.dbconn_prod_nba)

def getScoreboardDoc(dt): 
    url = 'http://espn.go.com/nba/scoreboard?date=%s' % dt.isoformat().replace('-','')
    response = urllib2.urlopen(url)
    return response.read()


def getGameIdsAndTeams(html, season):
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
            away_team_id = 0
            team_div = soup.findAll(id='%s-aTeamName' % game_id)
            if team_div and hasattr(team_div[0], 'a'):
                away_team_id, away_team, away_team_nbacom, away_team_nickname = findTeamName(team_div[0].a.renderContents(), season)

            home_team_id = 0
            team_div = soup.findAll(id='%s-hTeamName' % game_id)
            if team_div and hasattr(team_div[0], 'a'):
                home_team_id, home_team, home_team_nbacom, home_team_nickname = findTeamName(team_div[0].a.renderContents(), season)


            game_info.append(
                {'espn_game_id':game_id, 'away_team': away_team, 
                'home_team': home_team, 'away_team_nbacom': away_team_nbacom, 'home_team_nbacom': home_team_nbacom,
                'away_team_id': away_team_id, 'home_team_id': home_team_id, 
                'away_team_nickname': away_team_nickname, 'home_team_nickname': home_team_nickname
                }
            )
        except:
            print "Team not found. Skipping."



    return game_info


def findTeamName(name, season):
    teams = _getTeamData(season)
    
    for team in teams:
        if name == team['nickname'] or name == team['alternate_nickname']:
            return (team['id'], team['code'],team['nbacom_code'], team['nickname'])
        else:
            pass

    return (0,'unk','unk','unknown') 


def _getTeamData(season):
    result = dbobj.query_dict("SELECT * FROM team WHERE is_active = 1 AND season = '%s'" % (season)) 
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

def getUrl(url):
    response = urllib2.urlopen(url)
    return response.read()


def statsNbaCom(dt):
    dt_formatted = dt.strftime("%m/%d/%Y")
    url = 'http://stats.nba.com/stats/scoreboard/?LeagueID=00&gameDate=%s&DayOffset=0' % (dt_formatted)
    raw = getUrl(url)
    games = []
    
    data = json.loads(raw)
    for line in data['resultSets']:
        print line['name']
        if line['name'] == 'GameHeader':
            for row in line['rowSet']:
                games.append(dict(zip(line['headers'], row)))

    return games


def saveStatsNbaCom():
    dbobj = db.Db(config.dbconn_prod_nba)

    f = open('games.json','r')

    lines = f.readlines()
    for line in lines:
        data = json.loads(line.rstrip())
        if data:
            for row in data:
                sql = """
                    UPDATE game
                    SET national_tv = '%s',
                        statsnbacom_game_id = '%s',
                        gametime = '%s'
                    WHERE
                        nbacom_game_id = '%s'
                """ % (row['NATL_TV_BROADCASTER_ABBREVIATION'], row['GAME_ID'], row['GAME_STATUS_TEXT'], row['GAMECODE'])
                dbobj.query(sql)



def backfill():

    start_dt = datetime.date(2014,4,16)
    end_dt = datetime.date(2014,4,20)
    dt = start_dt
    f = open('games.json','a')

    while dt < end_dt:

        print dt
        f.write(json.dumps(statsNbaCom(dt)))
        f.write('\n')

        dt = dt + datetime.timedelta(days=1)
        time.sleep(3)



def main():
    dt = datetime.date(2014,1,25)
    statsNbaCom(dt)
    


def go(dt, season, season_type):
    
    html = getScoreboardDoc(dt)
    gamedata = getGameIdsAndTeams(html, season)
    complete_gamedata = _fillInGameData(season, season_type, gamedata, dt)

    for game in complete_gamedata:
        print game
        dbobj.insert_or_update('game',[game])
    



if __name__ == '__main__':
    saveStatsNbaCom()
