"""
Implementing chinese postman solver with pure Python.
"""
import sys
import time
from copy import deepcopy
from prettytable import PrettyTable

NOT_CONNECTED = 999
ZERO_WEIGHT = 0
PAUSE_DURATION = 0.5


class Node:
    def __init__(self, name):
        self.name = name

class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __str__(self):
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
        node1_index = self.nodes.index(node1)
        node2_index = self.nodes.index(node2)
        self.adjacency_matrix[node1_index][node2_index] = weight
        if not self.directed:
            self.adjacency_matrix[node2_index][node1_index] = weight

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
                        edges.append(Edge(
                            self.nodes[i],
                            self.nodes[j],
                            self.adjacency_matrix[i][j]))
                    else:
                        # sort the nodes if it's not directed graph
                        first_node = self.nodes[i]
                        second_node = self.nodes[j]
                        if first_node < second_node:
                            edges.append(Edge(
                                first_node,
                                second_node,
                                self.adjacency_matrix[i][j]))
                        else:
                            edges.append(Edge(
                                second_node,
                                first_node,
                                self.adjacency_matrix[i][j]))
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
                    distance_matrix[i][j] = min(
                        distance_matrix[i][j],
                        distance_matrix[i][k] + distance_matrix[k][j])
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
            # Must remove the edge from other node if it is not a
            # directed graph
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
        for i in range(len(self.nodes)):
            if self.directed:
                max_iteration = len(self.nodes)
            else:
                max_iteration = i
            for j in range(max_iteration):
                if self.adjacency_matrix[i][j] != NOT_CONNECTED:
                    print('%s-%s %s' % (
                        self.nodes[i],
                        self.nodes[j],
                        self.adjacency_matrix[i][j]))

    # FIXME: this method is broken
    def get_forward_nodes(self, node):
        node_index = self.nodes.index(node)
        print(node_index)
        forward_node_indexes = self.adjacency_matrix[node_index]
        forward_nodes = []
        for i, forward_node_index in enumerate(forward_node_indexes):
            if self.adjacency_matrix[node_index][forward_node_index] not in [
                    NOT_CONNECTED, ZERO_WEIGHT]:
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
                if self.adjacency_matrix[i][j] not in [
                        NOT_CONNECTED, ZERO_WEIGHT]:
                    adjacency_list[i].append(j)
        return adjacency_list


class HungarianSolver:
    """Class for running Hungarian algorithm.
    References:
    1. https://brc2.com/the-algorithm-workshop/
    2. https://towardsdatascience.com/maximizing-group-happiness-in-white-elephants-using-the-hungarian-optimal-assignment-algorithm-17be4f112746
    3. http://www.hungarianalgorithm.com/examplehungarianalgorithm.php
    """
    NORMAL = 0
    STARRED = 1
    PRIMED = 2

    def __init__(self, matrix):
        # Store original matrix
        self.original_matrix = matrix
        # Deep copy of the matrix so that the class does not alter the original
        self.matrix = deepcopy(self.original_matrix)
        # Mask matrix to cover the 0
        self.mask_matrix = deepcopy(self.original_matrix)
        length = len(self.mask_matrix)
        # Set all cell to Normal
        for i in range(length):
            for j in range(length):
                self.mask_matrix[i][j] = self.NORMAL
        self.row_covered = [False] * length
        self.column_covered = [False] * length
        self.current_step = 1
        self.finished = False
        # To store Z0 (uncovered zero on step 4)
        self.Z0_column = 0
        self.Z0_row = 0
        # Initialise path with size 2n x 2n, all 0
        self.path = []
        for i in range(2 * length):
            self.path.append([])
            for j in range(2 * length):
                self.path[i].append(0)

    def solve(self):
        self.finished = False
        self.current_step = 1
        while not self.finished:
            print('Step %s' % self.current_step)
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
            print('Row covered', self.row_covered)
            print('Column covered', self.column_covered)
            print_matrix(self.matrix)
            print_matrix(self.mask_matrix)
            time.sleep(PAUSE_DURATION)
        print('HungarianSolver finished.')

    def clear_covered(self):
        for i in range(len(self.matrix)):
            self.row_covered[i] = False
            self.column_covered[i] = False

    def step_1(self):
        """
        Step 1:  For each row of the matrix, find the smallest element and
        subtract it from every element in its row.  Go to Step 2.
        """
        for r in range(len(self.matrix)):
            min_row = min(self.matrix[r])
            for c in range(len(self.matrix)):
                self.matrix[r][c] -= min_row

        self.current_step = 2

    def step_2(self):
        """
        Step 2:  Find a zero (Z) in the resulting matrix.  If there is no
        starred zero in its row or column, star Z. Repeat for each element
        in the matrix. Go to Step 3.
        """
        length = len(self.matrix)
        for r in range(length):
            for c in range(length):
                if self.matrix[r][c] == 0 and \
                    not self.row_covered[r] and \
                        not self.column_covered[c]:
                    self.mask_matrix[r][c] = self.STARRED
                    # Covered the row and the column if the 0 found is the
                    # only (starred) zero on the row or column
                    self.row_covered[r] = True
                    self.column_covered[c] = True

        # Clear the covered because we need clear state of the covered
        self.clear_covered()

        self.current_step = 3

    def step_3(self):
        """
        Step 3:  Cover each column containing a starred zero.  If K columns
        are covered, the starred zeros describe a complete set of unique
        assignments.  In this case, Go to DONE, otherwise, Go to Step 4.
        """
        column_count = 0
        length = len(self.matrix)
        for row in range(length):
            for column in range(length):
                if self.mask_matrix[row][column] == self.STARRED and \
                    not self.column_covered[column]:
                    # Cover each column containing a starred zero
                    self.column_covered[column] = True
                    column_count += 1
        if column_count >= length:
            # All column is covered, then we have the solution.
            self.current_step = 7
        else:
            # Otherwise, go to step 4
            self.current_step = 4

    def find_uncovered_zero(self):
        """Find the first uncovered zero."""
        uncovered_zero_row = -1
        uncovered_zero_column = -1
        done = False
        row = 0

        while not done:
            column = 0
            while True:
                if self.matrix[row][column] == 0 and \
                    not self.row_covered[row] and \
                        not self.column_covered[column]:
                    uncovered_zero_row = row
                    uncovered_zero_column = column
                    done = True

                column += 1
                if column >= len(self.matrix) or done:
                    break
            row += 1
            if row >= len(self.matrix):
                done = True

        return uncovered_zero_row, uncovered_zero_column

    def find_star_in_row(self, row):
        """Find a starred element in the row. Return -1 if not found.
        """
        for c in range(len(self.matrix)):
            if self.mask_matrix[row][c] == self.STARRED:
                return c
        return -1

    def step_4(self):
        """
        Step 4:  Find a noncovered zero and prime it.  If there is no starred
        zero in the row containing this primed zero, Go to Step 5.  Otherwise,
        cover this row and uncover the column containing the starred zero.
        Continue in this manner until there are no uncovered zeros left.
        Save the smallest uncovered value and Go to Step 6.
        """
        row = 0
        column = 0
        done = False
        while not done:
            row, column = self.find_uncovered_zero()
            if row == -1:
                done = True
                self.current_step = 6
            else:
                self.mask_matrix[row][column] = self.PRIMED
                starred_column = self.find_star_in_row(row)
                if starred_column >= 0:
                    # Otherwise, cover this row and uncover the column
                    # containing the starred zero.
                    column = starred_column
                    self.row_covered[row] = True
                    self.column_covered[column] = False
                else:
                    # If there is no starred zero in the row containing this
                    # primed zero, Go to Step 5
                    done = True
                    self.Z0_column = column
                    self.Z0_row = row
                    self.current_step = 5

    def find_star_in_column(self, column):
        """Find a starred element in the column. Return -1 if not found.
        """
        for row in range(len(self.matrix)):
            if self.mask_matrix[row][column] == self.STARRED:
                return row
        return -1

    def find_prime_in_row(self, row):
        """Find a primed element in the row. Return -1 if not found.
        """
        for column in range(len(self.matrix)):
            if self.mask_matrix[row][column] == self.PRIMED:
                return column
        return -1

    def augment_path(self, path_count):
        for p in range(path_count):
            p_row = self.path[p][0]
            p_column = self.path[p][1]
            if self.mask_matrix[p_row][p_column] == self.STARRED:
                # Unstar each starred zero of the series
                self.mask_matrix[p_row][p_column] = self.NORMAL
            elif self.mask_matrix[p_row][p_column] == self.PRIMED:
                # star each primed zero of the series
                self.mask_matrix[p_row][p_column] = self.STARRED

    def erase_primes(self):
        """erase all primes"""
        for r in range(len(self.mask_matrix)):
            for c in range(len(self.mask_matrix)):
                if self.mask_matrix[r][c] == self.PRIMED:
                    self.mask_matrix[r][c] = self.NORMAL

    def step_5(self):
        """
        Construct a series of alternating primed and starred zeros as follows.
        Let Z0 represent the uncovered primed zero found in Step 4.
        Let Z1 denote the starred zero in the column of Z0 (if any).
        Let Z2 denote the primed zero in the row of Z1 (there will always be
        one).
        Continue until the series terminates at a primed zero that has no
        starred zero in its column. Unstar each starred zero of the series,
        star each primed zero of the series, erase all primes and uncover
        every line in the matrix. Return to Step 3.
        """
        done = False
        row = -1
        column = -1

        path_count = 0
        # Initialize path with uncovered primed zero (Z0)
        self.path[path_count][0] = self.Z0_row
        self.path[path_count][1] = self.Z0_column

        while not done:
            row = self.find_star_in_column(self.path[path_count][1])
            if row >= 0:
                # Found
                path_count += 1
                self.path[path_count][0] = row
                self.path[path_count][1] = self.path[path_count - 1][1]
            else:
                # No starred zero found in the column
                done = True
            if not done:
                column = self.find_prime_in_row(self.path[path_count][0])
                path_count += 1
                self.path[path_count][0] = self.path[path_count - 1][0]
                self.path[path_count][1] = column

        # Unstar each starred zero of the series,
        # star each primed zero of the series
        self.augment_path(path_count)
        # uncover every line in the matrix
        self.clear_covered()
        # erase all primes
        self.erase_primes()

        self.current_step = 3

    def find_smallest(self):
        smallest = sys.maxsize
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix)):
                if not self.row_covered[r] and not self.column_covered[c]:
                    if self.matrix[r][c] < smallest:
                        smallest = self.matrix[r][c]
        return smallest

    def step_6(self):
        """
        Step 6:  Add the value found in Step 4 to every element of each
        covered row, and subtract it from every element of each uncovered
        column.

        The value in step 4 is replaced by the smallest uncovered value.

        Return to Step 4 without altering any stars, primes, or covered lines.
        """
        # Find smallest uncovered value
        smallest = self.find_smallest()
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix)):
                if self.row_covered[r]:
                    # Row is covered, add smallest to it
                    self.matrix[r][c] += smallest
                if not self.column_covered[c]:
                    # Column is covered, substract smallest from it
                    self.matrix[r][c] -= smallest
                    if self.matrix[r][c] < -1:
                        raise Exception('Impossible to be negative')

        # Back to step 4
        self.current_step = 4

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
    # Example that after step 2 finished
    matrix = [
        [40, 60, 15],
        [25, 30, 45],
        [55, 25, 30]
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

def print_matrix(
        distance_matrix, column_names=None, row_names=None, first_cell=''):
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
    print("Adjacency matrix")
    print_matrix(graph.adjacency_matrix, graph.nodes)
    print("Floyd-Warshall distance matrix")
    print_matrix(graph.compute_floyd_warshall(), graph.nodes)
    print('Hungarian method')
    sample_hungarian()
    print('fin')
