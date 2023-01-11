# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import conf, re
from fabric import Connection
from paramiko.ssh_exception import AuthenticationException


def get_usage(user, computer, ssh):
    timekpra_userinfo_output = ssh.run(
            conf.ssh_timekpra_bin + ' --userinfo ' + user,
            hide=True
        )
    search = r"(ACTUAL_TIME_LEFT_DAY: )([0-9]+)"
    actual_time_left = re.search(search, str(timekpra_userinfo_output))
    # todo - better handle "else" when we can't find time remaining
    if actual_time_left and actual_time_left.group(2):
        print(f"time left for {user} at {computer}: " + str(actual_time_left.group(2)) + str(timekpra_userinfo_output))
    else:
        print(f"error! Could not get get usage for {user} at {computer}. SSH returned {str(actual_time_left)}")


def get_connection(computer):
    global connection
    # todo handle SSH keys instead of forcing it to be passsword only
    connect_kwargs = {
        'allow_agent': False,
        'look_for_keys': False,
        "password": conf.ssh_password
    }
    try:
        connection = Connection(
            host=computer,
            user=conf.ssh_user,
            connect_kwargs=connect_kwargs
        )
    except AuthenticationException as e:
        quit(f"Wrong credentials for user '{conf.ssh_user}' on host '{computer}'. "
              f"Check `ssh_user` and `ssh_password` credentials in config.py.")
    except Exception as e:
        quit(f"Error logging in as user '{conf.ssh_user}' on host '{computer}', check config. \n\n\t" + str(e))
    finally:
        return connection

def adjust_time(up_down_string, seconds, ssh, user):
    command = conf.ssh_timekpra_bin + ' --settimeleft ' + user + ' ' + up_down_string + ' ' + str(seconds)
    ssh.run(command)


def increase_time(seconds, ssh, user):
    adjust_time('+', seconds, ssh, user)
    print(f"added {str(seconds)} for user {user}")


def decrease_time(seconds, ssh, user):
    adjust_time('-', seconds, ssh, user)
    print(f"removed {str(seconds)} for user {user}")

def main():
    print('timetrkr-next-remote started')

    # todo - this should allow for more than one user per IP
    for ip in conf.trackme.keys():
        user = conf.trackme[ip]
        ssh = get_connection(ip)
        get_usage(user[0], ip, ssh)
        increase_time(100, ssh, user[0])
        get_usage(user[0], ip, ssh)
        decrease_time(100, ssh, user[0])
        get_usage(user[0], ip, ssh)


if __name__ == '__main__':
    main()
