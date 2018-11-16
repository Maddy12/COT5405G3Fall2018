import networkx as nx
import random
import matplotlib.pyplot as plt
from time import time
import pdb
from numpy import sum


def init_balanced_tree(branch_factor=2, height=4, max_weight=10):
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
    labels = nx.get_edge_attributes(graph, 'weight')
    # nx.draw(graph, pos, with_labels=True)
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    return graph, pos


def algorithm(layers=4, binary=True, brute_force=False, draw=False):
    """
    Goal is for that all path weight sums when subtracted = 0 i.e. L1-L2-L3=0
    We also want to minimize the path weight sums i.e. L1+L2+L3
    :param layers:
    :param binary:
    :return:
    """
    ### SET UP ###
    time_start = time()
    if binary:
        branch = 2
    else:
        branch = random.randint(2, 4)
    graph, pos = init_balanced_tree(branch_factor=branch, height=layers, max_weight=10)
    weight_dictionary = nx.get_edge_attributes(graph, 'weight')
    leafs = [leaf for leaf in graph.nodes if graph.degree(leaf) == 1]
    roots = [leaf for leaf in graph.nodes if graph.degree(leaf) > 1]
    path_lengths = get_path_lengths(leafs, graph, weight_dictionary)
    ### ALGORITHM - Brute Force ###
    if brute_force:
        node_pairs = list(weight_dictionary)
        node_pairs.sort()
        for idx in range(0, max(roots)*2 + 1, 2):
            edge_left = node_pairs[idx]
            edge_right = node_pairs[idx+1]
            # print("Running root {} for edges {} {}".format(node_pairs[idx][0], edge_left, edge_right))
            skew = weight_dictionary[edge_left] - weight_dictionary[edge_right]
            if skew < 0:
                weight_dictionary[node_pairs[idx]] += abs(skew)
            if skew > 0:
                weight_dictionary[node_pairs[idx+1]] += skew
        for edge in graph.edges:
             graph[edge[0]][edge[1]]['weight'] = weight_dictionary[edge]
        # nx.set_edge_attributes(graph, 'betweenness', weight_dictionary)
        time_end = time()
        diff = time_end - time_start

    ## ALGORITHM - Another Solution ##
    if not brute_force:
        leafs.sort()
        time_start = time()
        max_edge_length = max(path_lengths.values())
        for leaf in range(leafs[0], leafs[-1]+1):
            edge = list(graph.edges(leaf))[0]
            # print("Running leaf {} for edge {}".format(leaf, edge))
            current_path_length = path_lengths[leaf]
            additive_value = max_edge_length - current_path_length
            graph[edge[1]][edge[0]]['weight'] = weight_dictionary[(edge[1], edge[0])] + additive_value
            time_end = time()
            diff = time_end - time_start
    if draw:
        title = ['brute_force' if brute_force else 'algorithm']
        draw_tree(graph, pos, title[0])
    new_weight_dictionary = weight_dictionary = nx.get_edge_attributes(graph, 'weight')
    total_edge_sum = sum(new_weight_dictionary.values())
    results = test_results(leafs, graph)
    if not results:
        draw_tree(graph, pos, random.randint(1, 1000))
    print("Complete with runtime {}".format(diff))
    return diff, total_edge_sum, results


def test_results(leafs, graph):
    path_lengths = get_path_lengths(leafs, graph, nx.get_edge_attributes(graph, 'weight'))
    if len(set(path_lengths.values())) > 1:
        return False
    else:
        return True


def get_path_lengths(leafs, graph, weight_dictionary):
    path_lengths = dict()
    for leaf in leafs:
        if leaf == 0:
            continue
        paths = nx.all_simple_paths(graph, source=0, target=leaf)
        path = list(paths)[0]
        path_lengths[leaf] = get_edge_length(path, weight_dictionary)
    return path_lengths


def draw_tree(graph, pos, title):
    labels = nx.get_edge_attributes(graph, 'weight')
    fig = plt.figure()
    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    fig.savefig("{}.png".format(title))


def skew_and_sum(path_lengths):
    """
    The loss function we want to minimize.
    :param path_lengths:
    :return:
    """
    skew = path_lengths.values()[0]
    sum = path_lengths.values()[0]
    for p in path_lengths.values()[1:]:
        skew -= p
        sum += p
    return skew, sum


def get_edge_length(path, weight_dictionary):
    """
    Gets edge length for a given path to a leaf.
    :param path:
    :param weight_dictionary:
    :return:
    """
    l_e = 0
    for idx, node in enumerate(path):
        if idx+1 == len(path):
            continue
        l_e += weight_dictionary[(node, path[idx+1])]  # get edge weight of node 1 -> node 2
    return l_e


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
        diff, edge_sum, results = algorithm(layers=i, binary=True, brute_force=True)
        runtimes_brute_force.append(diff)
        edge_sum_brute_force.append(edge_sum)
        if not results:
            failures_brute_force[i] = diff
            print("Running another solution with {} layers".format(i))
        diff, edge_sum, results = algorithm(layers=i, binary=True, brute_force=False)
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

    plt.subplot(1, 2, 2)
    plt.plot(layers, edge_sum_algorithm, label='My Solution')
    plt.plot(layers, edge_sum_brute_force, label='Brute Force')
    plt.title("Comparing Brute Force to an Alternative Solution")
    plt.xlabel("Number of layers")
    plt.ylabel("Total Edge Sum")

    plt.savefig("comparison.png", dpi=300)
    plt.legend()
    plt.show()
    print(failures_algorithm)
    print(failures_brute_force)


if __name__ == "__main__":
    # draw_brute_force, results = algorithm(layers=4, binary=True, brute_force=True, draw=True)
    # draw_algorithm, results = algorithm(layers=4, binary=True, brute_force=False, draw=True)
    simulate(iterations=5)