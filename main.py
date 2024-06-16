# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import conf, re
from fabric import Connection
from paramiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError
from pathlib import Path

def get_config():
    return conf.trackme


def get_usage(user, computer, ssh):
    # to do - maybe check if user is in timekpr first? (/usr/bin/timekpra --userlist)
    global timekpra_userinfo_output
    fail_json = {'time_left': 0, 'time_spent': 0, 'result': 'fail'}
    try:
        timekpra_userinfo_output = str(ssh.run(
                conf.ssh_timekpra_bin + ' --userinfo ' + user,
                hide=True
            ))
    except NoValidConnectionsError as e:
        print(f"Cannot connect to SSH server on host '{computer}'. "
              f"Check address in conf.py or try again later.")
        return fail_json
    except AuthenticationException as e:
        print(f"Wrong credentials for user '{conf.ssh_user}' on host '{computer}'. "
              f"Check `ssh_user` and `ssh_password` credentials in conf.py.")
        return fail_json
    except Exception as e:
        quit(f"Error logging in as user '{conf.ssh_user}' on host '{computer}', check conf.py. \n\n\t" + str(e))
        return fail_json
    search = r"(TIME_LEFT_DAY: )([0-9]+)"
    time_left = re.search(search, timekpra_userinfo_output)
    search = r"(TIME_SPENT_DAY: )([0-9]+)"
    time_spent = re.search(search, timekpra_userinfo_output)
    # todo - better handle "else" when we can't find time remaining
    if not time_left or not time_left.group(2):
        print(f"Error getting time left, setting to 0. ssh call result: " + str(timekpra_userinfo_output))
        return fail_json
    else:
        time_left = str(time_left.group(2))
        time_spent = str(time_spent.group(2))
        print(f"Time left for {user} at {computer}: {time_left}")
        return {'time_left': time_left, 'time_spent': time_spent, 'result': 'success'}


def get_connection(computer):
    global connection
    # todo handle SSH keys instead of forcing it to be passsword only
    if conf.ssh_key.is_file() :
        connect_kwargs = {
            'allow_agent': False,
            'look_for_keys': False,
            'key_filename': conf.ssh_key
        }
        if conf.ssh_key_passphrase is defined and conf.ssh_key_passphrase is string :
            use_passphrase = { 'passphrase': conf.ssh_key_passphrase }
            connect_kwargs =  connect_kwargs | use_passphrase  

    else :
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
              f"Check `ssh_user` and `ssh_password` credentials in conf.py.")
    except Exception as e:
        quit(f"Error logging in as user '{conf.ssh_user}' on host '{computer}', check conf.py. \n\n\t" + str(e))
    finally:
        return connection

def adjust_time(up_down_string, seconds, ssh, user):
    command = conf.ssh_timekpra_bin + ' --settimeleft ' + user + ' ' + up_down_string + ' ' + str(seconds)
    ssh.run(command)
    if up_down_string == '-':
        print(f"added {str(seconds)} for user {user}")
    else:
        print(f"removed {str(seconds)} for user {user}")
    # todo - return false if this fails
    return True


def increase_time(seconds, ssh, user):
    return adjust_time('+', seconds, ssh, user)


def decrease_time(seconds, ssh, user):
    return adjust_time('-', seconds, ssh, user)


