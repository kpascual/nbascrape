import sys
import datetime
import time
import os
import MySQLdb
import logging
import importlib


from libscrape.config import constants

LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


def go(sourcedocs):

    for gamedata, files in sourcedocs:
        print "+++ EXTRACT: %s - %s" % (gamedata['id'], gamedata['abbrev'])

        for module, filename in files.items():
            print "  + %s" % (module)
            step_time = time.time()

            # Execute the module's default run() function, which implements the extract
            lib = importlib.import_module('extract.%s' % (module))
            getattr(lib,'run')(gamedata, filename)

            logging.info("EXTRACT - %s - game_id: %s - : time_elapsed %.2f" % (module, gamedata['id'], time.time() - step_time))



if __name__ == '__main__':
    sys.exit(main())
