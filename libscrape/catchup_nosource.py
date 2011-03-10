import master
import datetime


def main():

    #last = datetime.date.today() - datetime.timedelta(days=1)
    last = datetime.date(2010,10,28)

    first = datetime.date(2010,10,25)

    while first < last:
        master.restartFromExtract(first)
        first = first + datetime.timedelta(days=1)

if __name__ == '__main__':
    main()

