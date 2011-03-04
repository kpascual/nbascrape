import master
import datetime


def main():

    last = datetime.date(2011,2,26)

    first = datetime.date(2011,2,24)

    while first < last:
        master.getAll(first)
        first = first + datetime.timedelta(days=1)

if __name__ == '__main__':
    main()

