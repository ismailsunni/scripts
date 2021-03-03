"""
Implementing chinese postman solver with pure Python.
"""
from prettytable import PrettyTable
from copy import deepcopy

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
            for i in range(len(self.adjacency_matrix) - 1):
                self.adjacency_matrix[i].append(NOT_CONNECTED)
            # Self edge is zero
            self.adjacency_matrix[-1][-1] = ZERO_WEIGHT
        if node2 not in self.nodes:
            self.nodes.append(node2)
            # Add new column to the matrix
            self.adjacency_matrix.append([NOT_CONNECTED] * len(self.nodes))
            for i in range(len(self.adjacency_matrix) - 1):
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

    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    def compute_floyd_warshall(self):
        """Return the shortest distance matrix
        """
        distance_matrix = self.get_adjacency_matrix()
        for k in range(len(self.nodes)):
            for i in range(len(self.nodes)):
                for j in range(len(self.nodes)):
                    distance_matrix[i][j] = min(distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])
        return distance_matrix


    def compute_euler_cycle(self, start):
        """
        """
        # Use the index
        start = self.get_node_index(start)
        # Check if all nodes have even edges
        adjacency_list = self.get_adjacency_list()
        # Check if all nodes have even degree
        if sum([len(i) % 2 for i in adjacency_list]) != 0:
            return []
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


class HungarianSolver:
    """Class for running Hungarian algorithm.
    References:
    1. https://brc2.com/the-algorithm-workshop/
    2. https://towardsdatascience.com/maximizing-group-happiness-in-white-elephants-using-the-hungarian-optimal-assignment-algorithm-17be4f112746
    3. http://www.hungarianalgorithm.com/examplehungarianalgorithm.php
    """
    def __init__(self, matrix):
        # Store original matrix
        self.original_matrix = matrix
        # Deep copy of the matrix so that the class does not alter the original
        self.matrix = deepcopy(self.original_matrix)
        # Mask matrix to cover the 0
        self.mask_matrix = deepcopy(self.original_matrix)
        # Set all cell to False
        for i in range(len(self.mask_matrix)):
            for j in range(len(self.mask_matrix)):
                self.mask_matrix[i][j] = False
        self.row_covered = [False] * len(self.matrix)
        self.column_covered = [False] * len(self.matrix)
        self.current_step = 1
        self.finished = False

    def solve(self):
        self.finished = False
        self.current_step = 1
        while(not self.finished):
            print('Step %s' % self.current_step)
            print_matrix(self.matrix)
            if self.current_step == 1:
                self.step_1()
            elif self.current_step == 2:
                self.step_2()
            elif self.current_step == 3:
                self.step_3()
            elif self.current_step == 4:
                self.step_4()
            elif self.current_step == 5:
                self.step_5()
            elif self.current_step == 6:
                self.step_6()
            elif self.current_step == 7:
                self.step_7()
        print('HungarianSolver finished.')

    def step_1(self):
        # Step 1: Substract row minima
        for i in range(len(self.matrix)):
            min_row = min(self.matrix[i])
            for j in range(len(self.matrix)):
                self.matrix[i][j] = self.matrix[i][j] - min_row
        print('Step 1: substract row minima')
        print_matrix(self.matrix)
        # Step 1: Substract column minima
        for i in range(len(self.matrix)):
            min_column = min(row[i] for row in self.matrix)
            for j in range(len(self.matrix)):
                self.matrix[j][i] = self.matrix[j][i] - min_column
        print('Step 1: substract column minima')
        print_matrix(self.matrix)
        # Step 2: Cover zero
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0 and self.row_covered[i] == False and self.column_covered[j] == False:
                    self.mask_matrix[i][j] = True
                    self.row_covered[i] = True
                    self.column_covered[j] = True

        # reset cover ?
        for i in range(len(self.matrix)):
            self.row_covered[i] = False
            self.row_covered[j] = False

        self.current_step = 3

    def step_2(self):
        pass

    def step_3(self):
        # Step 3
        column_count = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.mask_matrix[i][j]:
                    self.column_covered[j] = True
        if self.column_covered.count(True) >= len(self.matrix):
            # Finihed
            self.current_step = 7
        else:
            # Go to step 4
            self.current_step = 4
            print('Not Implemented')
            print('Column cover != column number -> %s != %s' % (self.column_covered.count(True), len(self.matrix)))
            print_matrix(self.mask_matrix)

    def find_uncovered_zero(self):
        done = False
        row = 0
        column = 0
        zero_row = -1
        zero_column = -1
        while column < len(self.matrix) and not done:
            column = 0
            while column < len(self.matrix) and not done:
                if self.matrix[row][column] == 0 and self.row_covered[row] == False and self.column_covered[column] == False:
                    zero_column = column
                    zero_row = row
                    done = True
                column += 1
            row += 1

        if done:
            return zero_row, zero_column
        else:
            # Not found
            return -1, -1

    def step_4(self):
        row = -1
        column = -1
        done = False
        while not done:
            row, column = self.find_uncovered_zero()
            if row == -1:
                done = True
                self.current_step = 6
            else:
                pass

    def step_5(self):
        pass

    def step_6(self):
        pass

    def step_7(self):
        """Print the result"""
        pairs = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.mask_matrix[i][j]:
                    pairs.append((i, j))
        total = 0
        print('Pair result')
        for pair in pairs:
            print(pair)
            total += self.original_matrix[pair[0]][pair[1]]
        print('Total %s' % total)
        self.finished = True

def sample_hungarian():
    matrix = [
        [82, 83, 69, 92],
        [77, 37, 49, 92],
        [11, 69, 5, 86],
        [8, 9, 98, 23]
    ]
    matrix = [
        [40, 60, 15],
        [25, 30, 45],
        [55, 30, 25]
    ]
    matrix = [
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9]
    ]
    header = ['J%s' % i for i in range(len(matrix))]
    row_names = ['W%s' % i for i in range(len(matrix))]
    print_matrix(matrix, header, row_names)
    # matrix = compute_hungarian(matrix)
    hs = HungarianSolver(matrix)
    hs.solve()

def print_matrix(distance_matrix, column_names = None,  row_names = None, first_cell = ''):
    table = PrettyTable()
    if column_names:
        header = [first_cell]
        header.extend(column_names)
        table.field_names = header
    if not row_names:
        row_names = column_names
    for i in range(len(distance_matrix)):
        if row_names:
            row = [row_names[i]]
        else:
            row = []
        row.extend(distance_matrix[i])
        table.add_row(row)
    print(table)


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
    print("Adjacency matrix")
    print_matrix(graph.adjacency_matrix, graph.nodes)
    print("Floyd-Warshall distance matrix")
    print_matrix(graph.compute_floyd_warshall(), graph.nodes)
    print('Hungarian method')
    sample_hungarian()
    print('fin')