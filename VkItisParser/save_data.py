import psycopg2
from psycopg2 import OperationalError

sql = 'INSERT INTO "itis_group_words" values (%s, %s)'


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(database=db_name,
                                      user=db_user,
                                      password=db_password,
                                      host=db_host,
                                      port=db_port)
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def save(connection, word, count):
    cursor = connection.cursor()
    cursor.execute(sql, (word, count))
    connection.commit()
