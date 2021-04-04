import urllib

import requests
from bs4 import BeautifulSoup

from node import Node

global_nodes = {}
max_count = 2


class WebSpider:

    def __init__(self, node, id):
        self.id = id
        self.node = node
        self.parse()

    def get_links(self):
        try:
            resp = requests.get(self.node.link)
            soup = BeautifulSoup(resp.content, 'html.parser')
        except Exception:
            return []
        links = []
        for a in soup.find_all('a', href=True):
            new_link = urllib.parse.urljoin(self.node.link, a['href'])
            if new_link.endswith("/"):
                new_link = new_link[:-1]
            links.append(new_link)
            links = list(set(links))
        return links

    def get_last_links(self, node):
        resp = requests.get(node.link)
        soup = BeautifulSoup(resp.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            new_link = urllib.parse.urljoin(self.node.link, a['href'])
            if new_link.endswith("/"):
                new_link = new_link[:-1]
            if global_nodes.get(new_link) is not None:
                node.children.append(global_nodes[new_link])

    def parse(self):
        links = self.get_links()
        for link in links:
            if global_nodes.get(link) is None:
                if link.startswith("http"):
                    new_node = Node(link, len(global_nodes))
                    global_nodes[link] = new_node
                    if self.id < max_count:
                        WebSpider(new_node, self.id + 1)
                    else:
                        if self.id == max_count:
                            self.get_last_links(new_node)
                            continue
                    global_nodes[link].parents.append(self.node)
                    self.node.children.append(global_nodes[link])
