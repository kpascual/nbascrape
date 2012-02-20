import combine


def go(gamedata, dbobj):
    for game, files in gamedata:
        obj = combine.Combine(game, dbobj)
        obj.combineAll()
        print "Combined play-shot data for %s" % (game['abbrev'])


if __name__ == '__main__':
    go()
