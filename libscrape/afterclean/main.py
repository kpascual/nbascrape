import combine
import docs


def go(gamedata, dbobj):
    for game, files in gamedata:
        obj = combine.Combine(game, dbobj)
        obj.combineAll()
        print "Combined play-shot data for %s" % (game['abbrev'])

        print "Saving to CSV and JSON files"
        obj = docs.Docs(game, dbobj)
        obj.saveGamePlayShotToJson()
        obj.saveGamePlayShotToCsv()


if __name__ == '__main__':
    go()
