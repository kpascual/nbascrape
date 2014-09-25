import csv
import json
from libscrape.config import constants

LOGDIR_CLEAN = constants.LOGDIR_CLEAN

def run(filename, dbobj):
    data = open(constants.LOGDIR_CLEAN + filename, 'r').readlines()
    data = list(csv.reader(open(constants.LOGDIR_CLEAN + filename, 'r'),delimiter=',',lineterminator='\n'))
    fields = data[0]
    datapoints = data[1:]

    newdata = []
    for line in datapoints:
        newdata.append(dict(zip(fields,line)))
    
    dbobj.insert_or_update('boxscore_cbssports',newdata)
