"""
Implementing chinese postman solver with pure Python.
"""

NOT_CONNECTED = 999

class Graph:
    def __init__(self):
        self.nodes = []
        self.adjacency_matrix = []

    def add_edge(self, node1, node2, weight):
        if node1 not in self.nodes:
            # Add new node to list of nodes
            self.nodes.append(node1)
            # Add new column to the matrix
            self.adjacency_matrix.append([NOT_CONNECTED] * len(self.nodes))
            for i in range(len(self.adjacency_matrix)):
                self.adjacency_matrix[i].append(NOT_CONNECTED)
        if node2 not in self.nodes:
            self.nodes.append(node2)
            # Add new column to the matrix
            self.adjacency_matrix.append([NOT_CONNECTED] * len(self.nodes))
            for i in range(len(self.adjacency_matrix)):
                self.adjacency_matrix[i].append(NOT_CONNECTED)
        self.adjacency_matrix[self.nodes.index(node1)][self.nodes.index(node2)] = weight

    def print_graph(self):
        print('Nodes:')
        print(','.join(self.nodes))
        print('Adjacency matrix')
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.adjacency_matrix[i][j] != NOT_CONNECTED:
                    print(self.nodes[i], self.nodes[j], self.adjacency_matrix[i][j])

def read_graph(graph_file):
    """Read graph from file.
    The file format is:
    node1,node2,weight
    """
    data = None
    with open(graph_file) as file:
        data = file.read().splitlines()
    print(data)

    graph = Graph()
    for row in data:
        node1, node2, weight = row.split(',')
        print('Add edges: ', node1, node2, weight)
        graph.add_edge(node1, node2, int(weight))

    return graph

if __name__ == "__main__":
    graph_file = './simple_graph.csv'
    graph = read_graph(graph_file)
    graph.print_graph()


    print('fin')