import MySQLdb

dbconn_nba = {
    'user': 'username_for_database',
    'passwd': 'password_for_database',
    'db': 'name_of_database'
}


def nba_curs():
    conn = MySQLdb.connect(**dbconn_nba)
    curs = conn.cursor()
    
    return curs

def nba_query(qry):
    conn = MySQLdb.connect(**dbconn_nba)
    curs = conn.cursor()

    curs.execute(qry)

    return curs.fetchall()

def nba_query_dict(qry):
    conn = MySQLdb.connect(**dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute(qry)

    return curs.fetchall()

