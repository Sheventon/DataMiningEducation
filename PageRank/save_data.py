import configparser

import psycopg2


def delete_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS page_rank")


def create_table(cursor):
    cursor.execute('create table page_rank (link varchar not null, rank decimal(10, 9) not null)')


def add_link_to_table(cursor, key, value):
    cursor.execute("INSERT INTO page_rank (link, rank) VALUES (\'{}\', {})".format(str(key), value))


def save_to_data_base(result):
    config = configparser.ConfigParser()
    config.read('application.ini')
    database = config['EC2']['database']
    user = config['EC2']['user']
    password = config['EC2']['password']
    host = config['EC2']['host']
    port = config['EC2']['port']
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    delete_table(cursor)
    create_table(cursor)
    for (key, value) in result.items():
        add_link_to_table(cursor, key, value)
    conn.commit()
    conn.close()
