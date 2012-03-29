from libscrape.config import db
import datetime

dbobj = db.Db(db.dbconn_nba)


def getDiagnostics(dt):

    metric_funcs = [
        ('play_count_espn',getPlayCountEspn),
        ('shot_count_pbp_espn',getShotCountInPlayByPlayEspn),
        ('shot_count_cbssports',getShotCountCbsSports),
        ('shot_count_espn',getShotCountEspn),
        ('shot_count_nbacom',getShotCountNbaCom),
        ('unidentified_player_espn',getUnidentifiedPlayerCountEspn),
        ('unidentified_play_espn',getUnidentifiedPlaysCountEspn),
        ('game_count',getGameCount),
        ('matched_shots',checkMatchedShots),
        ('shot_orphans_espn',checkShotOrphansEspn),
        ('shot_orphans_cbssports',checkShotOrphansCbsSports),
        ('shot_orphans_nbacom',checkShotOrphansNbaCom),
    ]

    metrics = []
    for prefix, m in metric_funcs:
        #print "getting %s" % (m.__name__)
        result = m(dt)
        if type(result) is dict:
            for itm in result.items():
                if itm[0] == 'count':
                    metrics.append((prefix, itm[1]))
                else:
                    metrics.append(('%s_%s' % (prefix, itm[0]),itm[1]))
        else:
            metrics.append((prefix, result))

    _saveToDb(dt, metrics)


def _saveToDb(dt, data):
    for line in data:
        dbobj.query("""
            INSERT INTO rpt_diagnostics (metric, date, value)
            VALUES ('%s','%s',%s)
            ON DUPLICATE KEY UPDATE value = %s
        """ % (line[0], dt, line[1], line[1]))


def getPlayCountEspn(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*), COUNT(DISTINCT p.game_id)
        FROM playbyplay_espn p 
            INNER JOIN game g ON g.id = p.game_id 
        WHERE g.date_played = '%s'
    """ % (dt))

    if result:
        play_count, game_count = result[0]
    
        return {'count': play_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def getShotCountInPlayByPlayEspn(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*), COUNT(DISTINCT p.game_id)
        FROM playbyplay_espn p 
            INNER JOIN play_espn pe ON pe.id = p.play_espn_id
            INNER JOIN game g ON g.id = p.game_id 
        WHERE g.date_played = '%s' AND pe.is_shot = 1
    """ % (dt))

    if result:
        shot_count, game_count = result[0]
    
        return {'count': shot_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def getShotCountCbsSports(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*), COUNT(DISTINCT s.game_id)
        FROM shotchart_cbssports s
            INNER JOIN game g ON g.id = s.game_id 
        WHERE g.date_played = '%s'
    """ % (dt))

    if result:
        shot_count, game_count = result[0]
    
        return {'count': shot_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def getShotCountEspn(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*), COUNT(DISTINCT s.game_id)
        FROM shotchart_espn s
            INNER JOIN game g ON g.id = s.game_id 
        WHERE g.date_played = '%s'
    """ % (dt))

    if result:
        shot_count, game_count = result[0]
    
        return {'count': shot_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def getShotCountNbaCom(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*), COUNT(DISTINCT s.game_id)
        FROM shotchart_nbacom s
            INNER JOIN game g ON g.id = s.game_id 
        WHERE g.date_played = '%s'
    """ % (dt))

    if result:
        shot_count, game_count = result[0]
    
        return {'count': shot_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def getUnidentifiedPlayerCountEspn(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*), COUNT(DISTINCT p.game_id)
        FROM playbyplay_espn p
            INNER JOIN game g ON g.id = p.game_id 
        WHERE g.date_played = '%s'
            AND p.player_id = 0
    """ % (dt))

    if result:
        player_count, game_count = result[0]
    
        return {'count': player_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}
    

def getUnidentifiedPlaysCountEspn(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*), COUNT(DISTINCT p.game_id)
        FROM playbyplay_espn p
            INNER JOIN game g ON g.id = p.game_id 
        WHERE g.date_played = '%s'
            AND p.play_espn_id = 0
    """ % (dt))

    if result:
        play_count, game_count = result[0]
    
        return {'count': play_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def getGameCount(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT COUNT(*)
        FROM 
            game g 
        WHERE g.date_played = '%s'
    """ % (dt))

    if result:
        return result[0][0]
    else:
        return 0

def checkMatchedShots(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT 
            COUNT(shotchart_espn_id) espn,
            COUNT(shotchart_nbacom_id) nbacom,
            COUNT(shotchart_cbssports_id) cbssports
        FROM playshot ps
            INNER JOIN game g ON g.id = ps.game_id 
        WHERE g.date_played = '%s'
            AND ps.is_shot = 1
    """ % (dt))

    if result:
        espn, nbacom, cbssports = result[0]
    
        return {'espn': espn, 'nbacom': nbacom, 'cbssports': cbssports}
    else:
        return {'espn': 0, 'nbacom': 0, 'cbssports': 0}


def checkShotOrphansEspn(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT 
            COUNT(*), COUNT(DISTINCT g.id)
        FROM 
            shotchart_espn e 
            LEFT JOIN playshot ps ON e.id = ps.shotchart_espn_id
            INNER JOIN game g ON g.id = e.game_id 
        WHERE g.date_played = '%s'
            AND ps.playbyplay_espn_id IS NULL
    """ % (dt))

    if result:
        orphan_count, game_count = result[0]
    
        return {'count': orphan_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def checkShotOrphansCbsSports(dt):
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query("""
        SELECT 
            COUNT(*), COUNT(DISTINCT g.id)
        FROM 
            shotchart_cbssports e 
            LEFT JOIN playshot ps ON e.id = ps.shotchart_espn_id
            INNER JOIN game g ON g.id = e.game_id 
        WHERE g.date_played = '%s'
            AND ps.playbyplay_espn_id IS NULL
    """ % (dt))

    if result:
        orphan_count, game_count = result[0]
    
        return {'count': orphan_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def checkShotOrphansNbaCom(dt):

    result = dbobj.query("""
        SELECT 
            COUNT(*), COUNT(DISTINCT g.id)
        FROM 
            shotchart_nbacom e 
            LEFT JOIN playshot ps ON e.id = ps.shotchart_espn_id
            INNER JOIN game g ON g.id = e.game_id 
        WHERE g.date_played = '%s'
            AND ps.playbyplay_espn_id IS NULL
    """ % (dt))

    if result:
        orphan_count, game_count = result[0]
    
        return {'count': orphan_count, 'game_count': game_count}
    else:
        return {'count': 0, 'game_count': 0}


def getPlayEspnFrequency(dt):
    result = dbobj.query("""
        SELECT 
            pe.id, COUNT(*)
        FROM 
            playbyplay_espn pbp
            INNER JOIN play_espn pe ON pe.id = pbp.play_espn_id
            INNER JOIN game g ON g.id = pbp.game_id 
        WHERE g.date_played = '%s'
        GROUP BY 1
        ORDER BY COUNT(*) DESC
    """ % (dt))

    for line in result:
        dbobj.query("""
            INSERT INTO rpt_freq_play_espn (play_espn_id, date, value)
            VALUES (%s, '%s', %s)
            ON DUPLICATE KEY UPDATE value = %s
        """ % (line[0], dt, line[1], line[1]))


def getShotTypeNbaComFrequency(dt):
    result = dbobj.query("""
        SELECT 
            st.id, COUNT(*)
        FROM 
            playshot s
            INNER JOIN shot_type_nbacom st ON st.id = s.shot_type_nbacom_id
            INNER JOIN game g ON g.id = s.game_id 
        WHERE g.date_played = '%s'
        GROUP BY 1
        ORDER BY COUNT(*) DESC
    """ % (dt))


    for line in result:
        dbobj.query("""
            INSERT INTO rpt_freq_shot_type_nbacom (shot_type_nbacom_id, date, value)
            VALUES (%s, '%s', %s)
            ON DUPLICATE KEY UPDATE value = %s
        """ % (line[0], dt, line[1], line[1]))
    return result


def getShotTypeCbsSportsFrequency(dt):
    result = dbobj.query("""
        SELECT 
            st.id, COUNT(*)
        FROM 
            playshot s
            INNER JOIN shot_type_cbssports st ON st.id = s.shot_type_cbssports_id
            INNER JOIN game g ON g.id = s.game_id 
        WHERE g.date_played = '%s'
        GROUP BY 1
        ORDER BY COUNT(*) DESC
    """ % (dt))

    for line in result:
        dbobj.query("""
            INSERT INTO rpt_freq_shot_type_cbssports (shot_type_cbssports_id, date, value)
            VALUES (%s, '%s', %s)
            ON DUPLICATE KEY UPDATE value = %s
        """ % (line[0], dt, line[1], line[1]))

def go(dt):

    print "Getting diagnostic metrics..."
    getDiagnostics(dt)
    print "getting NBA.com shot type frequency"
    getShotTypeNbaComFrequency(dt)
    print "getting ESPN.com play type frequency"
    getPlayEspnFrequency(dt)
    print "getting CBSSports.com shot type frequency"
    getShotTypeCbsSportsFrequency(dt)


def main():
    dt = datetime.date.today() - datetime.timedelta(days=1)
    dt = datetime.date(2012,1,1)

    getDiagnostics(dt)
    getShotTypeNbaComFrequency(dt)
    getPlayEspnFrequency(dt)
    getShotTypeCbsSportsFrequency(dt)



if __name__ == '__main__':
    main()
