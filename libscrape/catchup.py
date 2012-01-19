import master
import datetime
import afterclean.fiveman

def checkClean():
    dt = datetime.date(2010,10,26)
    master.restartFromClean(dt)

def fillFiveman():

    for i in range(1,860):
        try:
            afterclean.fiveman.main(i)
            print "Fiveman for game %s completed" % i
        except:
            print "Couldn't find game %s" % i


def main():

    last = datetime.date(2010,10,31)

    first = datetime.date(2010,10,25)

    while first < last:
        master.restartFromExtract(first)
        first = first + datetime.timedelta(days=1)

if __name__ == '__main__':
    main()

