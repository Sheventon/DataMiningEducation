import collections
import configparser
import datetime as dt
import time

import requests
import psycopg2
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from psycopg2 import OperationalError

args = {
    'owner': 'shevanton',
    'start_date': dt.datetime(2021, 3, 15),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

sql = 'INSERT INTO "itis_words" values (%s, %s)'


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


def take_200_posts(token, version, domain):
    count = 100
    offset = 0
    all_posts = []

    while offset < 200:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                                )
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
        time.sleep(0.5)
    return all_posts


def write_to_file(data):
    with open('itis_kfu.txt', 'w', encoding='utf-8') as file:
        i = 1
        for post in data:
            file.write(post['text'] + '\n')
            try:
                file.write(post['copy_history'][0]['text'] + '\n')
            except Exception:
                pass
            file.write('\n')
            i += 1


def most_common_words(connection):
    file = open('itis_kfu.txt', encoding="utf-8")
    text = file.read()
    stop_symbols = r'.,:\!/?*-_•–—0123456789&"'
    wordcount = {}
    for word in text.lower().split():
        if word not in stop_symbols:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1

    n_print = int(input("How many most common words to print: "))
    print("\nOK. The {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(wordcount)
    for word, count in word_counter.most_common(n_print):
        save(connection, word, count)
        print(word, ": ", count)

    file.close()


def init_database():
    config = configparser.ConfigParser()
    config.sections()
    config.read('application.ini')
    db_name = config['LOCAL_DB']['db_name']
    db_user = config['LOCAL_DB']['db_user']
    db_password = config['LOCAL_DB']['db_password']
    db_host = config['LOCAL_DB']['db_host']
    db_port = config['LOCAL_DB']['db_port']
    return db_name, db_user, db_password, db_host, db_port


def init_vk():
    config = configparser.ConfigParser()
    config.sections()
    config.read('application.ini')
    token = config['VK']['token']
    version = config['VK']['version']
    domain = config['VK']['domain']
    return token, version, domain


def main():
    db_name, db_user, db_password, db_host, db_port = init_database()
    token, version, domain = init_vk()
    connection = create_connection(db_name, db_user, db_password, db_host, db_port)
    data = take_200_posts(token, version, domain)
    write_to_file(data)
    most_common_words(connection)


with DAG(dag_id='titanic_pivot', default_args=args, schedule_interval=None) as dag:
    main = PythonOperator(
        task_id='main',
        python_callable=main,
        dag=dag
    )
