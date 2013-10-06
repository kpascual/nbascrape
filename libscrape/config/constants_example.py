# Defines where you want intermediate dump files to be stored

LOGDIR_EXTRACT = '/your_path_here/dump/extract/'
LOGDIR_SOURCE = '/your_path_here/dump/source/'
LOGDIR_CLEAN = '/your_path_here/dump/clean/'
LOGDIR_LOAD = '/your_path_here/dump/load/'
LOGDIR_AFTERCLEAN = '/your_path_here/dump/afterclean/'
LOGDIR_DOCS = '/your_path_here/dump/docs/'

URL_SHOTCHART_CBSSPORTS = 'http://www.cbssports.com/nba/gametracker/shotchart/NBA_'
URL_PLAYBYPLAY_ESPN = 'http://espn.go.com/nba/playbyplay?gameId=<game_id>&period=0'
URL_SHOTCHART_ESPN = 'http://sports.espn.go.com/nba/gamepackage/data/shot?gameId=<game_id>'
URL_PLAYBYPLAY_NBACOM = 'http://www.nba.com/games/game_component/dynamic/<game_id>/pbp_all.xml'
URL_SHOTCHART_NBACOM = 'http://www.nba.com/games/game_component/dynamic/<game_id>/shotchart_all.xml'
URL_BOXSCORE_NBACOM = 'http://www.nba.com/games/game_component/dynamic/<game_id>/boxscore.xml'

URL = {
    'nba': {
        'SHOTCHART_CBSSPORTS': 'http://www.cbssports.com/nba/gametracker/shotchart/NBA_',
        'PLAYBYPLAY_ESPN': 'http://espn.go.com/nba/playbyplay?gameId=<game_id>&period=0',
        'SHOTCHART_ESPN': 'http://sports.espn.go.com/nba/gamepackage/data/shot?gameId=<game_id>',
        'PLAYBYPLAY_NBACOM': 'http://www.nba.com/games/game_component/dynamic/<game_id>/pbp_all.xml',
        'SHOTCHART_NBACOM': 'http://www.nba.com/games/game_component/dynamic/<game_id>/shotchart_all.xml',
        'BOXSCORE_NBACOM': 'http://www.nba.com/games/game_component/dynamic/<game_id>/boxscore.xml'
    },
    'wnba': {
        'PLAYBYPLAY_ESPN': 'http://espn.go.com/wnba/playbyplay?gameId=<game_id>&period=0',
        'SHOTCHART_ESPN': 'http://sports.espn.go.com/wnba/gamepackage/data/shot?gameId=<game_id>',
        'PLAYBYPLAY_NBACOM': 'http://www.wnba.com/games/game_component/dynamic/<game_id>/pbp_all.xml',
        'SHOTCHART_NBACOM': 'http://www.wnba.com/games/game_component/dynamic/<game_id>/shotchart_all.xml',
        'BOXSCORE_NBACOM': 'http://www.wnba.com/games/game_component/dynamic/<game_id>/boxscore.xml'
    }
}

LIST_TEAMS = ['MILWAUKEE', 'MINNESOTA', 'MIAMI', 'ATLANTA', 'BOSTON', 'DETROIT', 'DENVER', 'NEW JERSEY', 'NEW ORLEANS', 'DALLAS', 'PORTLAND', 'ORLANDO', 'TORONTO', 'CHICAGO', 'NEW YORK', 'CHARLOTTE', 'UTAH', 'GOLDEN STATE', 'CLEVELAND', 'HOUSTON', 'WASHINGTON', 'LOS ANGELES', 'PHILADELPHIA', 'PHOENIX', 'MEMPHIS', 'LOS ANGELES', 'SACRAMENTO', 'OKLAHOMA CITY', 'INDIANA', 'SAN ANTONIO']

SECONDS = {
    'nba': {
        'game_regulation': 2880,
        'in_quarter': 720,
        'in_overtime': 300
    },
    'wnba': {
        'game_regulation': 2400,
        'in_quarter': 600,
        'in_overtime': 300
    },
}

"""
PERIODS = [
    '1 Quarter',
    '2 Quarter',
    '3 Quarter',
    '4 Quarter',
    '1 Overtime',
    '2 Overtime',
    '3 Overtime',
    '4 Overtime',
    '5 Overtime',
    '6 Overtime',
    '7 Overtime',
    '8 Overtime',
    '9 Overtime',
    '10 Overtime',
    '11 Overtime',
    '12 Overtime',
    '13 Overtime',
    '14 Overtime',
    '15 Overtime'
]
"""
PERIODS = {
    '1 Quarter': 1,
    '2 Quarter': 2,
    '3 Quarter': 3,
    '4 Quarter': 4,
    '1 Overtime': 5,
    '2 Overtime': 6,
    '3 Overtime': 7,
    '4 Overtime': 8,
    '5 Overtime': 9,
    '6 Overtime': 10,
    '7 Overtime': 11,
    '8 Overtime': 12,
    '9 Overtime': 13,
    '10 Overtime': 14,
    '11 Overtime': 15,
    '12 Overtime': 16,
    '5 Quarter': 5,
    '6 Quarter': 6,
    '7 Quarter': 7,
    '8 Quarter': 8,
    '9 Quarter': 9,
    '10 Quarter': 10,
    '11 Quarter': 11,
    '12 Quarter': 12,
    '13 Quarter': 13,
    '14 Quarter': 14,
    '15 Quarter': 15,
    '16 Quarter': 16,
}

