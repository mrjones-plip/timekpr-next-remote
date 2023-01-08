# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import subprocess, sqlite3, time, conf, os
from datetime import datetime
from sqlite3 import Error
from fabric import Connection

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    sqlite = None
    try:
        sqlite = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    try:
        create_table_sql = """ CREATE TABLE IF NOT EXISTS status (
                id integer PRIMARY KEY,
                name text NOT NULL,
                state text NOT NULL,
                date text
            ); """
        c = sqlite.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    return sqlite


def get_user_usage(user, computer):


def main():
    sqlite = create_connection(r"./timetrkr-next-remote.db")
    print('timetrkr-next-remote started')


if __name__ == '__main__':
    main()
