import networkx as nx
from networkx import degree_sequence_tree as tree
import random
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
from time import time
from collections import OrderedDict
import pdb

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


def algorithm(layers=4, binary=True):
    """
    Goal is for that all path weight sums when subtracted = 0 i.e. L1-L2-L3=0
    We also want to minimize the path weight sums i.e. L1+L2+L3
    :param layers:
    :param binary:
    :return:
    """
    ### SET UP ###
    if binary:
        branch = 2
    else:
        branch = random.randint(2, 4)
    graph, pos = init_balanced_tree(branch_factor=branch, height=layers, max_weight=10)
    weight_dictionary = nx.get_edge_attributes(graph, 'weight')
    leafs = [leaf for leaf in graph.nodes if graph.degree(leaf) == 1]
    roots = [leaf for leaf in graph.nodes if graph.degree(leaf) > 1]
    path_lengths = dict()
    for leaf in leafs:
        if leaf == 0:
            continue
        paths = nx.all_simple_paths(graph, source=0, target=leaf)
        path = list(paths)[0]
        path_lengths[leaf] = get_edge_length(path, weight_dictionary)
    time_start = time()
    ### ALGORITHM ###
    node_pairs = list(weight_dictionary)
    node_pairs.sort()
    for root in range(0, max(roots) + 1, 2):
        edge_left = node_pairs[root]
        edge_right = node_pairs[root+1]
        skew = weight_dictionary[edge_left] - weight_dictionary[edge_right]
        if skew < 0:
            weight_dictionary[edge_left] += abs(skew)
        if skew > 0:
            weight_dictionary[edge_right] += skew
    for edge in graph.edges:
         graph[edge[0]][edge[1]]['weight'] = weight_dictionary[edge]
    # nx.set_edge_attributes(graph, 'betweenness', weight_dictionary)
    draw_tree(graph, pos)
    time_end = time()
    return weight_dictionary, graph


def draw_tree(graph, pos):
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)


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


if __name__ == "__main__":
    algorithm()
