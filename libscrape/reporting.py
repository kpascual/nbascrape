import datetime
import feedback.daily


def go(dt):
    feedback.daily.getDiagnostics(dt)
    feedback.daily.getShotTypeNbaComFrequency(dt)
    feedback.daily.getPlayEspnFrequency(dt)
    feedback.daily.getShotTypeCbsSportsFrequency(dt)


def main():

    try:
        dt = sys.argv[1]
        dt = datetime.date(*map(int,dt.split('-')))
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)

    print dt
    feedback.daily.go(dt)
    

if __name__ == '__main__':
    main()
