class TransictionMatrix:

    def __init__(self, global_nodes):
        self.nodes = global_nodes
        self.matrix = [[0] * (len(global_nodes) + 1) for i in range((len(global_nodes) + 1))]
        self.dumping_factor = 0.85
        self.vector = []
        for element in range(len(self.nodes)):
            self.vector.append(1 / len(self.nodes))

        print(len(self.nodes))
        print(len(self.vector))

        self.fill_matrix()

    def fill_matrix(self):
        for key in self.nodes:
            my_node = self.nodes.get(key)
            count = float(len(my_node.children))
            for i in range(len(my_node.children) - 1):
                child_id = my_node.children[i].id
                self.matrix[my_node.id][child_id] = self.dumping_factor / count

    def multiply_matrix(self):
        for k in range(20):
            new_vector = self.vector
            for i in range(len(self.matrix) - 1):
                count = 0.0
                for j in range(len(self.matrix[i]) - 1):
                    count += self.vector[j] * self.matrix[j][i]
                new_vector[i] = count + (1 - self.dumping_factor) / len(new_vector)
            self.vector = new_vector

        page_rank_map = {}
        for key in self.nodes:
            node = self.nodes[key]
            page_rank_map[node.link] = self.vector[node.id]

        page_rank_map = {k: v for k, v in sorted(page_rank_map.items(),
                                                 key=lambda item: item[1],
                                                 reverse=True)}
        return page_rank_map
