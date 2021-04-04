import configparser

import psycopg2


def deleteTable(cursor):
    cursor.execute("DROP TABLE IF EXISTS page_rank")


def createTable(cursor):
    cursor.execute('create table page_rank (link varchar not null, rank decimal(10, 9) not null)')


def addLinkToTable(cursor, key, value):
    cursor.execute("INSERT INTO page_rank (link, rank) VALUES (\'{}\', {})".format(str(key), value))


def saveToDataBase(result):
    config = configparser.ConfigParser()
    config.read('application.ini')
    database = config['DB']['database']
    user = config['DB']['user']
    password = config['DB']['password']
    host = config['DB']['host']
    port = config['DB']['port']
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    deleteTable(cursor)
    createTable(cursor)
    for (key, value) in result.items():
        addLinkToTable(cursor, key, value)
    conn.commit()
    conn.close()
