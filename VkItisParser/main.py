import collections
import requests
import time
import configparser
from save_data import create_connection
from save_data import save


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

    n_print = 100
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
    db_name = config['DB']['db_name']
    db_user = config['DB']['db_user']
    db_password = config['DB']['db_password']
    db_host = config['DB']['db_host']
    db_port = config['DB']['db_port']
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


if __name__ == '__main__':
    main()
