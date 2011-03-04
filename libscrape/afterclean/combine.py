from libscrape.config import db

def combine(game_id = 52):
    shots = db.nba_query_dict("""
        SELECT sh.*, s.name as shot_name, s.is_freethrow 
        FROM shottest sh INNER JOIN cbsshot s ON s.id = sh.shot_type_id WHERE sh.game_id = %s
    """ % game_id)
    pbp = db.nba_query_dict("""
        SELECT pbp.*, p.is_shot, p.name 'play_name', p.is_freethrow
        FROM pbptest pbp INNER JOIN play p ON pbp.play_id = p.id 
        WHERE pbp.game_id = %s
    """ % game_id)
    shots = list(shots)
    pbp = list(pbp)
 
    counter = 0 
    combined = []
    for row in pbp:
        # Get list of shots that may qualify
        if row['is_shot'] == 1:
            possible = [(i,shot) for i,shot in enumerate(shots) if row['team_code'] == shot['team_code'] and row['player_id'] == shot['player_id'] \
                and (row['sec_elapsed_game'] - shot['sec_elapsed_game'] <= 30 and row['sec_elapsed_game'] - shot['sec_elapsed_game'] >= -10)] 

            if len(possible) == 1:
                matched_shot = possible[0]
                del shots[possible[0][0]]

            elif len(possible) > 1: 
                if row['is_freethrow'] == 1:
                    new_possible = [(idx,itm) for idx,itm in possible if itm['is_freethrow'] == 1]
                    
                    # Assume the first free throw item is sufficient
                    if new_possible:
                        matched_shot = new_possible[0]
                        del shots[new_possible[0][0]]
                    else:
                        print "something went wrong here... no matched free throw found!"
                else:
                    # Just take the first item
                    matched_shot = possible[0]
                    del shots[possible[0][0]]

            row['x'] = matched_shot[1]['x']
            row['y'] = matched_shot[1]['y']
            row['distance_shotchart'] = matched_shot[1]['distance']
            row['cbs_shot_type_id'] = matched_shot[1]['shot_type_id']
            row['shot_num_shotchart'] = matched_shot[1]['shot_num']

        del row['is_freethrow']
        del row['is_shot']
        del row['play_name']

        combined.append(row)
    
    return combined

def insert(data):
    for itm in data:
        fields = ','.join(map(str,sorted(itm.keys())))
        values = "'" + "','".join(map(str,[v for k,v in sorted(itm.items())])) + "'"
        sql = """INSERT INTO combined (%s) VALUES (%s) """  % (fields, values)
        db.nba_query(sql)


def main(game_id = 10):
    #gamedata = db.nba_query("SELECT id, away_team, home_team FROM game WHERE id = %s" % game_id)
    result = combine()
    insert(result)


if __name__ == '__main__':
    main()
