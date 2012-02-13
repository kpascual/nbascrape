from libscrape.config import db
import json
import datetime

import libscrape.config.constants

LOGDIR_AFTERCLEAN = libscrape.config.constants.LOGDIR_AFTERCLEAN

class Combine:
    def __init__(self, gamedata):
        self.gamedata = gamedata
        self.filename = self.gamedata['abbrev'] + '_combined'
        self.game_id = self.gamedata['id']


    def appendCbsSportsShotsToEspnPlayByPlay(self):
        shots_cbssports = self._getCbsSportsShots()
        shots = shots_cbssports[:]
        playbyplay_espn = self._getEspnPlayByPlay()

        combined = self._appendShots(shots_cbssports, playbyplay_espn)
        combined = self._translateCbsSportsShotFields(combined, shots)
        combined = self._cleanEspnPlayByPlayFields(combined)

        self._writeToDatabase('playshot_cbssports', combined)
        self._writeToFile(LOGDIR_AFTERCLEAN + self.filename + '_cbssports', combined)
        

    def appendEspnShotsToEspnPlayByPlay(self):
        shots_espn = self._getEspnShots()
        shots = shots_espn[:]
        playbyplay_espn = self._getEspnPlayByPlay()

        combined = self._appendShots(shots_espn, playbyplay_espn)
        combined = self._translateEspnShotFields(combined, shots)
        combined = self._cleanEspnPlayByPlayFields(combined)

        self._writeToDatabase('playshot_espn', combined)
        self._writeToFile(LOGDIR_AFTERCLEAN + self.filename + '_espn', combined)
        

    def appendNbaComShotsToEspnPlayByPlay(self):
        shots_nbacom = self._getNbaComShots()
        shots = shots_nbacom[:]
        playbyplay_espn = self._getEspnPlayByPlay()

        combined = self._appendShots(shots_nbacom, playbyplay_espn)
        combined = self._translateNbaComShotFields(combined, shots)
        combined = self._cleanEspnPlayByPlayFields(combined)

        self._writeToDatabase('playshot_nbacom', combined)
        self._writeToFile(LOGDIR_AFTERCLEAN + self.filename + '_nbacom', combined)


    def createCombinedPlayShot(self):
        db.nba_query("""
            INSERT INTO playshot
            SELECT * 
            FROM
                playshot_espn
            WHERE
                game_id = %s
        """ % (self.game_id))
        db.nba_query("""
            UPDATE playshot ps
                INNER JOIN playshot_nbacom psnbacom 
                    ON psnbacom.game_id = ps.game_id AND psnbacom.playbyplay_espn_id = ps.playbyplay_espn_id
            SET
                ps.shotchart_nbacom_id = psnbacom.shotchart_nbacom_id,
                ps.shot_type_nbacom_id = psnbacom.shot_type_nbacom_id,
                ps.shotchart_nbacom_x = psnbacom.shotchart_nbacom_x,
                ps.shotchart_nbacom_y = psnbacom.shotchart_nbacom_y
            WHERE ps.game_id = %s
        """ % (self.game_id))
        db.nba_query("""
            UPDATE playshot ps
                INNER JOIN playshot_cbssports pscbs
                    ON pscbs.game_id = ps.game_id AND pscbs.playbyplay_espn_id = ps.playbyplay_espn_id
            SET
                ps.shotchart_cbssports_id = pscbs.shotchart_cbssports_id,
                ps.shot_type_cbssports_id = pscbs.shot_type_cbssports_id,
                ps.shotchart_cbssports_x = pscbs.shotchart_cbssports_x,
                ps.shotchart_cbssports_y = pscbs.shotchart_cbssports_y
            WHERE ps.game_id = %s
        """ % (self.game_id))


    def _appendShots(self, shots, playbyplay):
    
        suggested_matches = []
        combined = []
        combineresult = []
        for play in playbyplay:

            newplay = dict(play.items())
            matchingresults = play
            # Get list of shots that may qualify
            if play['is_shot'] == 1:

                possible_matched_shots = self._findShotMatches(play, shots) 
                matchingresults['shot_matches'] = possible_matched_shots

                foundShot = len(possible_matched_shots) >= 1
                play['shot_matches'] = []
                if foundShot:

                    match = self._chooseBestMatch(possible_matched_shots, shots, play)
                    shots = match['shots']
                    #matchingresults['best_shot_match'] = match['matched_shot'] 

                    newplay['x'] = match['matched_shot']['shot_data']['x']
                    newplay['y'] = match['matched_shot']['shot_data']['y']
                    newplay['shot_id'] = match['matched_shot']['shot_data']['id']
                    newplay['distance_playbyplay_espn'] = newplay['distance']
                    del newplay['distance']
                    del newplay['is_freethrow']

            newplay['playbyplay_espn_id'] = play['id']
            del newplay['play_name']
            del newplay['home_play_desc']
            del newplay['away_play_desc']

            combined.append(newplay)
            combineresult.append(play)
 
     
        return combined


    def _chooseBestMatch(self, matched_shots, shots, play):
        if len(matched_shots) == 1:
            matched_shot = matched_shots[0]

            # Remove shot data from pool of unmatched shots
            del shots[matched_shot['shot_index']]

        elif len(matched_shots) > 1: 
            matched_shot = matched_shots[0]
            # Create a new routine to determine best match                        
            if 'is_freethrow' in play.keys() and play['is_freethrow'] == 1:
                    new_possible = []
                    try:
                        new_possible = [line for line in matched_shots if line['shot_data']['is_freethrow'] == 1]
                        # Assume the first free throw item is sufficient
                        matched_shot = new_possible[0]
                        del shots[new_possible[0]['shot_index']]
                    except:
                        print "something went wrong here... no matched free throw found! play number %s" % play['play_num']
            else:
            
                # Just take the first item
                matched_shot = matched_shots[0]
                del shots[matched_shot['shot_index']]

        return {'matched_shot': matched_shot, 'shots': shots}

    
    def _translateCbsSportsShotFields(self, playshots, shots):
        new_playshots = []
        for line in playshots:
            if 'shot_id' in line.keys():
                line['shotchart_cbssports_id'] = line['shot_id']
                line['shotchart_cbssports_x'] = line['x']
                line['shotchart_cbssports_y'] = line['y']

                for shot in shots:
                    if int(shot['id']) == int(line['shot_id']):
                        line['shot_type_cbssports_id'] = shot['shot_type_cbssports_id']
                        line['is_shot_made'] = shot['is_shot_made']

                del line['shot_id']
                del line['x']
                del line['y']

            new_playshots.append(line)
    
        return new_playshots


    def _translateNbaComShotFields(self, playshots, shots):
        new_playshots = []
        for line in playshots:
            if 'shot_id' in line.keys():
                line['shotchart_nbacom_id'] = line['shot_id']
                line['shotchart_nbacom_x'] = line['x']
                line['shotchart_nbacom_y'] = line['y']

                
                for shot in shots:
                    if int(shot['id']) == int(line['shot_id']):
                        line['shot_type_nbacom_id'] = shot['shot_type_nbacom_id']
                        line['is_shot_made'] = shot['is_shot_made']

                del line['shot_id']
                del line['x']
                del line['y']

            new_playshots.append(line)
    
        return new_playshots


    def _translateEspnShotFields(self, playshots, shots):
        new_playshots = []
        for line in playshots:
            if 'shot_id' in line.keys():
                line['shotchart_espn_id'] = line['shot_id']
                line['shotchart_espn_x'] = line['x']
                line['shotchart_espn_y'] = line['y']

                for shot in shots:
                    if int(shot['id']) == int(line['shot_id']):
                        line['is_shot_made'] = shot['is_shot_made']

                del line['shot_id']
                del line['x']
                del line['y']

            new_playshots.append(line)
    
        return new_playshots
        

    def _cleanEspnPlayByPlayFields(self, playshots):
        new_playshots = []
        for line in playshots:
            if 'distance' in line.keys():
                line['distance_playbyplay_espn'] = line['distance']

                del line['distance']

            del line['id']
            if 'is_freethrow' in line.keys():
                del line['is_freethrow']
            if 'is_shot' in line.keys():
                del line['is_shot']
            if 'is_shot_made' in line.keys():
                del line['is_shot_made']

            new_playshots.append(line)
    
        return new_playshots
        


    def _dumpSuggestedMatches(self, data):
        f = open('suggested_matches.txt','w')
        shot_json = json.dumps(data, indent=2, sort_keys=True)
        f.write(shot_json)


    def _findShotMatches(self, play_data, shot_data):

        possible_shots = []
        for shot_index, shot_data in enumerate(shot_data):
            isSameTeam = play_data['team_id'] == shot_data['team_id']
            isSamePlayer = play_data['player_id'] == shot_data['player_id'] 
            isSameShotResult = play_data['is_shot_made'] == shot_data['is_shot_made']

            time_diff = (play_data['deciseconds_left'] - shot_data['deciseconds_left'])
            isWithinTimeFrame = time_diff <= 300 and time_diff >= -100 and play_data['period'] == shot_data['period']

            if isSameTeam and isSamePlayer and isWithinTimeFrame and isSameShotResult:
                possible_shots.append({'shot_index':shot_index,'shot_data':shot_data})

        return possible_shots


    def _getCbsSportsShots(self):
        return list(db.nba_query_dict("""
            SELECT sh.*, s.name as shot_name, s.is_freethrow 
            FROM shotchart_cbssports sh 
                INNER JOIN shot_type_cbssports s ON s.id = sh.shot_type_cbssports_id WHERE sh.game_id = %s
        """ % self.game_id))


    def _getNbaComShots(self):
        return list(db.nba_query_dict("""
            SELECT s.*
            FROM shotchart_nbacom s
            WHERE s.game_id = %s
        """ % self.game_id))


    def _getEspnShots(self):
        return list(db.nba_query_dict("""
            SELECT s.*
            FROM shotchart_espn s
            WHERE s.game_id = %s
        """ % self.game_id))


    def _getEspnPlayByPlay(self):
        return list(db.nba_query_dict("""
            SELECT pbp.id as 'playbyplay_espn_id', pbp.*, 
                p.is_shot, p.name 'play_name', p.is_freethrow, p.is_shot_made
            FROM playbyplay_espn pbp 
                INNER JOIN play_espn p ON pbp.play_espn_id = p.id 
            WHERE pbp.game_id = %s
        """ % self.game_id))


    def _writeToFile(self, filename, data):
        f = open(filename,'w')
        shot_json = json.dumps(data, indent=2, sort_keys=True)
        f.write(shot_json)

        
    def _writeToDatabase(self, table_name, data):
        for line in data:
            headers = [key for key,val in sorted(line.items())]
            quoted_values = ['"%s"' % (val) for key,val in sorted(line.items())]
            duplicate_key_clauses = ['%s="%s"' % (key,val) for key,val in sorted(line.items())]
    
            db.nba_query("""
                INSERT INTO %s
                (%s)
                VALUES (%s)
                ON DUPLICATE KEY UPDATE
                %s
            """ % (table_name, ','.join(headers), ','.join(quoted_values),','.join(duplicate_key_clauses)))

        
    def insert(self, data):
        for itm in data:
            fields = ','.join(map(str,sorted(itm.keys())))
            values = "\"" + "\",\"".join(map(str,[v for k,v in sorted(itm.items())])) + "\""
            sql = """INSERT INTO combined (%s) VALUES (%s) """  % (fields, values)
            db.nba_query(sql)


def main(game_id = 1499):
    gamedata = db.nba_query_dict("SELECT * FROM game WHERE id = %s" % (game_id))[0]
    obj = Combine(gamedata)

    obj.appendCbsSportsShotsToEspnPlayByPlay()
    obj.appendEspnShotsToEspnPlayByPlay()
    obj.appendNbaComShotsToEspnPlayByPlay()



def catchup():
    last = datetime.date(2012,2,11)
    first = datetime.date(2010,10,25)
    
    while first < last:
        
        games = db.nba_query_dict("SELECT * FROM game WHERE date_played = '%s'" % (first))
        for gamedata in games:
            print gamedata['abbrev']
            obj = Combine(gamedata)

            obj.appendCbsSportsShotsToEspnPlayByPlay()
            obj.appendEspnShotsToEspnPlayByPlay()
            obj.appendNbaComShotsToEspnPlayByPlay()
            obj.createCombinedPlayShot()

        first = first + datetime.timedelta(days=1)



if __name__ == '__main__':
    catchup()
    #fillAllGames()
