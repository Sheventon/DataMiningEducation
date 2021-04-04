class Node:
    def __init__(self, link, id):
        self.id = id
        self.link = link
        self.children = []
        self.parents = []
        self.pagerank = 1.0
