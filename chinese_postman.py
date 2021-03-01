"""
Implementing chinese postman solver with pure Python.
"""

NOT_CONNECTED = 999
ZERO_WEIGHT = 0


class Node:
    def __init__(self, name):
        self.name = name

class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __str__ (self):
        return "%s-%s %s" % (self.node1, self.node2, self.weight)

class Graph:
    def __init__(self, directed=False):
        self.nodes = []
        self.adjacency_matrix = []
        self.directed = directed

    def add_edge(self, node1, node2, weight):
        if node1 not in self.nodes:
            # Add new node to list of nodes
            self.nodes.append(node1)
            # Add new column to the matrix
            self.adjacency_matrix.append([NOT_CONNECTED] * len(self.nodes))
            for i in range(len(self.adjacency_matrix)):
                self.adjacency_matrix[i].append(NOT_CONNECTED)
            # Self edge is zero
            self.adjacency_matrix[-1][-1] = ZERO_WEIGHT
        if node2 not in self.nodes:
            self.nodes.append(node2)
            # Add new column to the matrix
            self.adjacency_matrix.append([NOT_CONNECTED] * len(self.nodes))
            for i in range(len(self.adjacency_matrix)):
                self.adjacency_matrix[i].append(NOT_CONNECTED)
            # Self edge is zero
            self.adjacency_matrix[-1][-1] = ZERO_WEIGHT
        self.adjacency_matrix[self.nodes.index(node1)][self.nodes.index(node2)] = weight
        if not self.directed:
            self.adjacency_matrix[self.nodes.index(node2)][self.nodes.index(node1)] = weight

    def get_edges(self):
        edges = []
        for i in range(len(self.nodes)):
            if self.directed:
                max_iteration = len(self.nodes)
            else:
                max_iteration = i
            for j in range(max_iteration):
                if self.adjacency_matrix[i][j] != NOT_CONNECTED:
                    if self.directed:
                        edges.append(Edge(self.nodes[i], self.nodes[j], self.adjacency_matrix[i][j]))
                    else:
                        # sort the nodes if it's not directed graph
                        first_node = self.nodes[i]
                        second_node = self.nodes[j]
                        if first_node < second_node:
                            edges.append(Edge(first_node, second_node, self.adjacency_matrix[i][j]))
                        else:
                            edges.append(Edge(second_node, first_node, self.adjacency_matrix[i][j]))
        return edges

    def get_node_index(self, node):
        return self.nodes.index(node)

    def compute_euler_cycle(self, start):
        """
        """
        # Use the index
        start = self.get_node_index(start)
        # Check if all nodes have even edges
        adjacency_list = self.get_adjacency_list()
        euler_cycle = [start]
        current_node = start
        prev_node = None
        num_edges = sum([len(i) for i in adjacency_list])
        while num_edges > 0:
            prev_node = current_node
            # go to the next node
            current_node = adjacency_list[current_node].pop()
            num_edges -= 1
            # Must remove the edge from other node if it is not a directed graph
            if not self.directed:
                num_edges -= 1
                adjacency_list[current_node].remove(prev_node)
            euler_cycle.append(current_node)
        # Return with labels
        return [self.nodes[x] for x in euler_cycle]

    def print_graph(self):
        print('Directed: %s' % self.directed)
        print('Nodes: %s' % ','.join(self.nodes))
        print('Adjacency matrix:')
        edges = self.get_edges
        for i in range(len(self.nodes)):
            if self.directed:
                max_iteration = len(self.nodes)
            else:
                max_iteration = i
            for j in range(max_iteration):
                if self.adjacency_matrix[i][j] != NOT_CONNECTED:
                    print('%s-%s %s' % (self.nodes[i], self.nodes[j], self.adjacency_matrix[i][j]))

    # FIXME: Broken
    def get_forward_nodes(self, node):
        node_index = self.nodes.index(node)
        print(node_index)
        forward_node_indexes = self.adjacency_matrix[node_index]
        forward_nodes = []
        for i, forward_node_index in enumerate(forward_node_indexes):
            if self.adjacency_matrix[node_index][forward_node_index] not in [NOT_CONNECTED, ZERO_WEIGHT]:
                forward_nodes.append(self.nodes[i])
        return forward_nodes

    def get_adjacency_list(self):
        """Return adjacency list of the graph. Only stores the index.
        """
        adjacency_list = []
        for i in range(len(self.nodes)):
            adjacency_list.append([])
            for j in range(len(self.nodes)):
                if i == j:
                    continue
                if self.adjacency_matrix[i][j] not in [NOT_CONNECTED, ZERO_WEIGHT]:
                    adjacency_list[i].append(j)
        return adjacency_list


def read_graph(graph_file):
    """Read graph from file.
    The file format is:
    node1,node2,weight
    """
    data = None
    with open(graph_file) as file:
        data = file.read().splitlines()

    graph = Graph()
    for row in data:
        node1, node2, weight = row.split(',')
        graph.add_edge(node1, node2, int(weight))

    return graph

if __name__ == "__main__":
    graph_file = './simple_graph.csv'
    graph = read_graph(graph_file)
    graph.print_graph()
    node_1 = graph.nodes[0]
    print('First node %s' % node_1)
    # neighbour_nodes_1 = graph.get_forward_nodes(node_1)
    # print(neighbour_nodes_1)
    print('Edges in the graph')
    for e in graph.get_edges():
        print(e)
    adjacency_list = graph.get_adjacency_list()
    print('Adjacency list, index based')
    for node in adjacency_list:
        print(node)
    print('Euler cycle')
    euler_cycle = graph.compute_euler_cycle(node_1)
    print(euler_cycle)

    print('fin')