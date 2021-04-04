from node import Node
from save_data import saveToDataBase
from transiction_matrix import TransictionMatrix
from web_spider import WebSpider, global_nodes

main_url = 'https://mcdonalds.ru'


if __name__ == '__main__':
    node = Node(main_url, 0)
    global_nodes[node.link] = node
    spider = WebSpider(node, 0)
    matrix = TransictionMatrix(global_nodes)
    result = matrix.multiply_matrix()
    saveToDataBase(result)
