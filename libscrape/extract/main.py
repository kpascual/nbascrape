import sys
import datetime
import os

import pbp_espn


LOGDIR_SOURCE = '../../logs/source/'
LOGDIR_EXTRACT = '../../logs/extract/'


def getDate():
    try:
        dt =  sys.argv[1]
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)
        dt = dt.isoformat()
    
    return dt


def writeToFile(filename, list_plays):
    f = open(LOGDIR_EXTRACT + filename, 'w')
    f.write('\n'.join([','.join([str(point) for point in play]) for play in list_plays]))
    f.close()


def main():
    dt = getDate()
    
    files = {}
    files_playbyplay = [f for f in os.listdir(LOGDIR_SOURCE) if dt in f and 'pbp_espn' in f]
    files_shotchart = [f for f in os.listdir(LOGDIR_SOURCE) if dt in f and 'shotchart_cbssports' in f]
   
 
    for f in files_playbyplay:
        # Scrape ESPN play by play data
        print f
        list_plays = pbp_espn.Extract(open(LOGDIR_SOURCE + f,'r').read(), f).extractAll()
        writeToFile(f,list_plays) 
    """
    for f in files_shotchart:
        # Scrape CBS Sports shot chart data
        list_files_shotchart = cbssports_shotchart.main(game_data)
        files['shotchart'].append(list_files_shotchart) 
    """

if __name__ == '__main__':
    sys.exit(main())
