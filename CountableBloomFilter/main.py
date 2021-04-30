import math
import random

import mmh3
from urllib.request import urlopen
from bs4 import BeautifulSoup

false_positive = 0.0001


class CountableBloomFilter:

    def __init__(self, items_count, fp):
        self.fp = fp
        self.size = self.get_size(items_count, self.fp)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.bit_array = [0] * self.size

    @staticmethod
    def get_size(n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def get_hash_count(m, n):
        k = (m / n) * math.log(2)
        return math.ceil(k)

    def add_item(self, item):
        digests = []
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)
            self.bit_array[digest] += 1

    def check_item(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == 0:
                return False
        return True


def test():
    url = "https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%81%D1%81%D0%B8,_%D0%9B%D0%B8%D0%BE%D0%BD%D0%B5%D0%BB%D1%8C"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.find_all('p')
    data = []

    for word in text:
        data.extend(word.getText().split(' '))

    data_len = len(data)
    cbf = CountableBloomFilter(data_len, false_positive)

    for word in data:
        cbf.add_item(word)

    print("Size of filter: {}".format(cbf.size))
    print("False positive probability: {}".format(cbf.fp))
    print("Number of hash functions: {}".format(cbf.hash_count))
    print("------------------------------------------------")

    random_words = []
    for i in range(0, 10):
        random_index = random.randint(0, len(data) - 1)
        random_words.append(data[random_index])
        if cbf.check_item(random_words[i]):
            print('Word <' + random_words[i] + '> contains in text')
        else:
            print('Word ' + random_words[i] + ' is not contains in text')


if __name__ == '__main__':
    test()
