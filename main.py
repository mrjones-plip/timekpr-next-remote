# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import conf
from fabric import Connection


def get_usage(user, computer):
    result = Connection(computer, user='root').run('/usr/bin/timekpra --userinfo ' + user)
    print(result)


def main():
    print('timetrkr-next-remote started')

    for ip in conf.trackme.keys():
        # todo - this should allow for more than one user per IP
        user = conf.trackme[ip]
        get_usage(user[0], ip)


if __name__ == '__main__':
    main()
