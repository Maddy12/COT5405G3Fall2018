import networkx as nx
import random
import matplotlib.pyplot as plt
from time import time
import pdb
from numpy import sum


class BinaryTree(object):

    def __init__(self, layers=4):
        """
        Goal is for that all path weight sums when subtracted = 0 i.e. L1-L2-L3=0
        We also want to minimize the path weight sums i.e. L1+L2+L3
        :param layers:
        :param binary:
        :return:
        """
        self.__time_start = time()

        self.graph, self.__pos = self._init_balanced_tree(branch_factor=2, height=layers, max_weight=10)
        self.weight_dictionary = nx.get_edge_attributes(self.graph, 'weight')
        self.leafs = [leaf for leaf in self.graph.nodes if self.graph.degree(leaf) == 1]
        self.roots = [leaf for leaf in self.graph.nodes if self.graph.degree(leaf) > 1]
        self.path_lengths = self.get_path_lengths()

    def _init_balanced_tree(self, branch_factor=2, height=4, max_weight=10):
        """
        Uses networkx to quickly initialize a balanced tree.
        Then we randomly add weights to the edges.
        :param branch_factor: Split nodes by
        :param height: How many layers in the tree
        :param max_weight: When randomly initializing edge weights, what is the max weight
        :return:
        """
        graph = nx.balanced_tree(branch_factor, height)
        pos = nx.spring_layout(graph)
        for edge in graph.edges:
            graph[edge[0]][edge[1]]['weight'] = random.randint(1, max_weight)
        return graph, pos

    def update_weight_dictionary(self):
        self.weight_dictionary = nx.get_edge_attributes(self.graph, 'weight')

    def get_path_lengths(self):
        path_lengths = dict()
        for leaf in self.leafs:
            if leaf == 0:
                continue
            paths = nx.all_simple_paths(self.graph, source=0, target=leaf)
            path = list(paths)[0]
            self.update_weight_dictionary()
            path_lengths[leaf] = self.get_edge_length(path)
        return path_lengths

    def draw_tree(self, title):
        labels = nx.get_edge_attributes(self.graph, 'weight')
        fig = plt.figure()
        nx.draw(self.graph, self.__pos, with_labels=True)
        nx.draw_networkx_edge_labels(self.graph, self.__pos, edge_labels=labels)
        fig.savefig("{}.png".format(title))

    def get_edge_length(self, path):
        """
        Gets edge length for a given path to a leaf.
        :param path:
        :param weight_dictionary:
        :return:
        """
        l_e = 0
        for idx, node in enumerate(path):
            if idx + 1 == len(path):
                continue
            l_e += self.weight_dictionary[(node, path[idx + 1])]  # get edge weight of node 1 -> node 2
        return l_e


def run_algorithms(layers, brute_force=True, draw=False):
    tree = BinaryTree(layers)
    graph = tree.graph
    if draw:
        title = ['before_brute_force' if brute_force else 'before_algorithm']
        tree.draw_tree(title[0])
    time_start = time()
    ### ALGORITHM - Brute Force ###
    if brute_force:
        previous_nodes = [0]
        for layer in range(1, layers+1):
            paths = dict()
            new_previous_nodes = list()
            for node in previous_nodes:
                # pdb.set_trace()
                for path in list(graph.edges(node)):
                    if path[0] < path[1]:
                        new_previous_nodes.append(path[1])
                        paths[path] = tree.weight_dictionary[path]
            previous_nodes = new_previous_nodes
            max_d = max(paths.values())
            for path, d in paths.items():
                if d < max_d:
                    graph[path[0]][path[1]]['weight'] = tree.weight_dictionary[path] + (max_d - tree.weight_dictionary[path])
        time_end = time()
        diff = time_end - time_start

    ## ALGORITHM - Another Solution ##
    if not brute_force:
        tree.leafs.sort()
        time_start = time()
        max_edge_length = max(tree.path_lengths.values())
        for leaf in range(tree.leafs[0], tree.leafs[-1]+1):
            edge = list(graph.edges(leaf))[0]
            # print("Running leaf {} for edge {}".format(leaf, edge))
            current_path_length = tree.path_lengths[leaf]
            additive_value = max_edge_length - current_path_length
            graph[edge[1]][edge[0]]['weight'] = tree.weight_dictionary[(edge[1], edge[0])] + additive_value
            time_end = time()
            diff = time_end - time_start
    if draw:
        title = ['after_brute_force' if brute_force else 'after_algorithm']
        tree.draw_tree(title[0])
    new_weight_dictionary = nx.get_edge_attributes(graph, 'weight')
    total_edge_sum = sum(new_weight_dictionary.values())
    results = test_results(tree)
    if not results:
        tree.draw_tree(random.randint(1, 1000))
    print("Complete with runtime {}".format(diff))
    return diff, total_edge_sum, results


def test_results(tree):
    path_lengths = tree.get_path_lengths()  # nx.get_edge_attributes(tree.graph, 'weight'))
    if len(set(path_lengths.values())) > 1:
        return False
    else:
        return True


def simulate(iterations):
    runtimes_algorithm = list()
    edge_sum_algorithm = list()
    failures_algorithm = dict()
    runtimes_brute_force = list()
    edge_sum_brute_force = list()
    failures_brute_force = dict()
    layers = range(2, iterations+2)
    for i in layers:
        print("Running brute force algorithm with {} layers".format(i))
        diff, edge_sum, results = run_algorithms(layers=i, brute_force=True)
        runtimes_brute_force.append(diff)
        edge_sum_brute_force.append(edge_sum)
        if not results:
            failures_brute_force[i] = diff
            print("Running another solution with {} layers".format(i))
        diff, edge_sum, results = run_algorithms(layers=i, brute_force=False)
        runtimes_algorithm.append(diff)
        edge_sum_algorithm.append(edge_sum)
        if not results:
            failures_algorithm[i] = diff
    plt.subplot(1,2,1)
    plt.plot(layers, runtimes_algorithm, label='My Solution')
    plt.plot(layers, runtimes_brute_force, label='Brute Force')
    for x, y in failures_algorithm.items():
        plt.plot(x, y, color='red', marker="o")
    for x, y in failures_brute_force.items():
        plt.plot(x, y, color='red', marker="o")
    plt.xlabel("Number of layers")
    plt.ylabel("Runtimes (ms)")
    plt.legend()
    plt.savefig("comparison_runtimes.png", dpi=300)
    plt.show()

    plt.plot(layers, edge_sum_algorithm, label='My Solution')
    plt.plot(layers, edge_sum_brute_force, label='Brute Force')
    plt.title("Comparing Brute Force to an Alternative Solution")
    plt.xlabel("Number of layers")
    plt.ylabel("Total Edge Sum")
    plt.legend()
    plt.savefig("comparison_edge_sum.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    diff, total_edge_sum, results = run_algorithms(layers=4, brute_force=True, draw=True)
    diff, total_edge_sum, results = run_algorithms(layers=4, brute_force=False, draw=True)
    simulate(iterations=15)