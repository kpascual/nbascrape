from libscrape.config import db
from libscrape.config import constants
import json
import csv


class Docs:
    def __init__(self, gamedata, dbobj):
        self.dbobj = dbobj
        self.gamedata = gamedata
        self.game_id = self.gamedata['id']
        self.away_team = self.gamedata['away_team_id']
        self.home_team = self.gamedata['home_team_id']
        self.date_played = self.gamedata['date_played']
        self.game_name = self.gamedata['abbrev']


    def saveGamePlayShotToJson(self):
        result = self.dbobj.query_dict("""
            SELECT ps.*, pe.is_rebound, pe.is_assist, pe.is_shot, pe.is_shot_made, pe.is_freethrow,
                pe.is_foul, pe.is_turnover
            FROM playshot ps INNER JOIN play_espn pe ON pe.id = ps.play_espn_id 
            WHERE ps.game_id = %s
        """ % (self.game_id))

        contents = json.dumps(result)
        f = open(constants.LOGDIR_DOCS + self.game_name + '_playshot.json','w')
        f.write(contents)
        f.close()


    def saveGamePlayShotToCsv(self):
        result = self.dbobj.query_dict("""
            SELECT ps.*, pe.is_rebound, pe.is_assist, pe.is_shot, pe.is_shot_made, pe.is_freethrow,
                pe.is_foul, pe.is_turnover
            FROM playshot ps INNER JOIN play_espn pe ON pe.id = ps.play_espn_id 
            WHERE ps.game_id = %s
        """ % (self.game_id))

        headers = [row[0] for row in sorted(result[0].items())]
        data = [line[1] for row in result for line in sorted(row.items())]
        data = []
        for row in result:
            newline = []
            for line in sorted(row.items()):
                newline.append(line[1])

            data.append(newline)
            

        writer = csv.writer(open(constants.LOGDIR_DOCS + self.game_name + '_playshot.csv','w'),delimiter=',',lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        writer.writerows([headers] + data)
        
        


def main(game_id = 1500):
    gamedata = self.dbobj.query_dict("SELECT * FROM game WHERE id = %s" % game_id)
    obj = Docs(gamedata[0])
    
    obj.saveGamePlayShotToJson()
    obj.saveGamePlayShotToCsv()


if __name__ == '__main__':
    main()
