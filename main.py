# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import conf, re
from fabric import Connection


def get_usage(user, computer):
    # todo - put this in try/except for when the command fails
    timekpra_userinfo_output = Connection(computer, user=conf.ssh_user).\
        run(conf.ssh_timekpra_bin + ' --userinfo ' + user, hide=True)

    # todo - remove this sample output
    # ACTUAL_TIME_SPENT_DAY: 0
    # ACTUAL_TIME_LEFT_DAY: 3600
    # ACTUAL_TIME_LEFT_CONTINUOUS: 3600
    # ACTUAL_PLAYTIME_LEFT_DAY: 0

    search = r"(ACTUAL_TIME_LEFT_DAY: )(\d{4})"
    actual_time_left = re.search(search, str(timekpra_userinfo_output))
    # todo - handle "else" when we can't find time remaining
    if actual_time_left and actual_time_left.group(2):
        print(f"time left for {user} at {computer}: " + str(actual_time_left.group(2)) )


def main():
    print('timetrkr-next-remote started')

    for ip in conf.trackme.keys():
        # todo - this should allow for more than one user per IP
        user = conf.trackme[ip]
        get_usage(user[0], ip)


if __name__ == '__main__':
    main()
