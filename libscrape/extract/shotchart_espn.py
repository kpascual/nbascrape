from libscrape.config import constants
from BeautifulSoup import BeautifulStoneSoup
import csv
import re
import shutil
import os

LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT
LOGDIR_SOURCE = constants.LOGDIR_SOURCE


# Extract file for NBA.com related files is a trivial move of the source XML files
# They're already well-defined, no use in messing with it.

def copyFile(filename):
    shutil.copyfile(LOGDIR_SOURCE + filename, LOGDIR_EXTRACT + filename)

def main():
    files = [f for f in os.listdir(LOGDIR_SOURCE) if 'shotchart_espn' in f]
    for f in files:
        copyFile(f)


if __name__ == '__main__':
    main()
        

