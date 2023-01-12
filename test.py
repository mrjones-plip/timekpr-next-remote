import main
import conf, re
from fabric import Connection
from paramiko.ssh_exception import AuthenticationException

def go():
    print('timetkpr-next-remote started')

    # todo - this should allow for more than one user per IP
    for ip in conf.trackme.keys():
        user = conf.trackme[ip]
        ssh = main.get_connection(ip)
        main.get_usage(user[0], ip, ssh)
        main.increase_time(100, ssh, user[0])
        main.get_usage(user[0], ip, ssh)
        main.decrease_time(100, ssh, user[0])
        main.get_usage(user[0], ip, ssh)


if __name__ == '__main__':
    go()
