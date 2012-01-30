import MySQLdb

# Pass these data structures as params to the DB class
dbconn_prod = {
    'user': 'username_for_database',
    'passwd': 'password_for_database',
    'db': 'production_database_name'
}


dbconn_test = {
    'user': 'username_for_database',
    'passwd': 'password_for_database',
    'db': 'test_or_staging_database_name'
}

class Db:

    def __init__(self, credentials):
        self.credentials = credentials
        self.conn = MySQLdb.connect(**credentials)
        

    def query(self, sql):
        curs = self.curs()
        curs.execute(sql)
        
        return curs.fetchall()


    def curs(self):
        return self.conn.cursor()


    def query_dict(self, sql):
        curs = self.conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(sql)
        
        return curs.fetchall()



