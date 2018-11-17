from __future__ import print_function
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os


#### Network Simulation ###
def init_graph():
    """
    Creates a graph with one node and one self-loop
    :return:
    """
    graph = nx.Graph()
    graph.add_node(1)
    graph.add_edge(1, 1)
    return graph


def run_simulation(p_births, simulations, time_steps, time_steps_collect, t_degree=4000):
    """
    For each probability, it runs a number of simulations, each of a network evolution for t timesteps.
    The number of nodes, edges, and degree disributions are averaged over each simulation and returned in a dictionary.
    :param p_births:
    :param simulations:
    :param time_steps:
    :param time_steps_collect:
    :param t_degree:
    :return:
    """
    num_nodes = dict()
    num_edges = dict()
    degree_dist_dict = list()
    # Iterate through each probability passed
    for p in p_births:
        # Run the number of simulations passed
        steps_nodes = {"step1": 0, "step2": 0, "step3": 0, "step4": 0, "step5": 0}
        steps_edges = {"step1": 0, "step2": 0, "step3": 0, "step4": 0, "step5": 0}
        degree_hist = dict()
        for simulation in range(simulations):
            graph = init_graph()  # re-initialize for each simulation
            nodes_t_list = list()
            edges_t_list = list()
            # for t in progressbar.progressbar(range(1, time_steps + 1)):  # iterate network evolution over t timesteps
            for t in range(1, time_steps + 1):  # iterate network evolution over t timesteps
                print("Running {} simulation {} ---- timestep {}/{}".format(p, simulation+1, t, time_steps), end='\r')
                if len(graph.nodes) == 0 or len(graph.edges) == 0:
                    graph = init_graph()
                try:
                    nodes = graph.number_of_nodes()
                    edges = graph.number_of_edges()
                    # This is to decide if a new node will be born or a node will die, either one must take place
                    birth = np.random.choice([True, False], p=[p, 1 - p])
                    new_node = None
                    if birth:
                        new_node = max(graph.nodes) + 1  # just name the node after the maximum nodes + 1
                    # This is to decide if a node will die
                    preferential_attach = dict()
                    preferential_death = dict()
                    for node in graph.nodes():
                        if birth:
                            d_node = graph.degree(node)
                            d_network = 2.0 * edges
                            # p_u = (nodes - d_node)/(nodes**2 - d_network)
                            p_u = d_node / d_network
                            preferential_attach[node] = p_u
                        if not birth:
                            d_node = graph.degree(node)
                            d_network = 2.0 * graph.number_of_edges()
                            # p_u = (nodes - d_node) / ((nodes ** 2) - d_network)
                            try:
                                p_u = (d_network - d_node) / (d_network * (nodes - 1))
                            except ZeroDivisionError:
                                p_u = 1
                            preferential_death[node] = p_u
                    if birth:
                        node_new_edge = np.random.choice(preferential_attach.keys(), p=preferential_attach.values())
                        graph.add_edge(new_node, node_new_edge)
                    if not birth:
                        node_die = np.random.choice(preferential_death.keys(), p=preferential_death.values())
                        graph.remove_node(node_die)
                    graph_nodes = graph.number_of_nodes()
                    nodes_t_list.append(graph_nodes)
                    edges_t_list.append(graph.number_of_edges())
                    if t == t_degree and p == .8:  # only happens at one time stamp
                        degree_hist = nx.degree_histogram(graph)
                        print(degree_hist)
                except Exception as e:
                    error = e
                    nx.draw(graph, node_size=1, node_color='b')
                    import pdb;
                    pdb.set_trace()
            steps_nodes['step1'] = nodes_t_list[time_steps_collect[0] - 1] + steps_nodes['step1']
            steps_nodes['step2'] = nodes_t_list[time_steps_collect[1] - 1] + steps_nodes['step2']
            steps_nodes['step3'] = nodes_t_list[time_steps_collect[2] - 1] + steps_nodes['step3']
            steps_nodes['step4'] = nodes_t_list[time_steps_collect[3] - 1] + steps_nodes['step4']
            steps_nodes['step5'] = nodes_t_list[time_steps_collect[4] - 1] + steps_nodes['step5']
            steps_edges['step1'] = edges_t_list[time_steps_collect[0] - 1] + steps_edges['step1']
            steps_edges['step2'] = edges_t_list[time_steps_collect[1] - 1] + steps_edges['step2']
            steps_edges['step3'] = edges_t_list[time_steps_collect[2] - 1] + steps_edges['step3']
            steps_edges['step4'] = edges_t_list[time_steps_collect[3] - 1] + steps_edges['step4']
            steps_edges['step5'] = edges_t_list[time_steps_collect[4] - 1] + steps_edges['step5']
            # sum up all the simulation runs
            if p == .8:
                try:
                    degree_sum_dist = [sum(x) for x in zip(degree_sum_dist, degree_hist)]
                except NameError:
                    print("False")
                    degree_sum_dist = np.zeros(len(degree_hist))
                    degree_sum_dist = [sum(x) for x in zip(degree_sum_dist, degree_hist)]

        num_nodes[str(p)] = {time_steps_collect[0]: steps_nodes['step1'] / simulations,
                             time_steps_collect[1]: steps_nodes['step2'] / simulations,
                             time_steps_collect[2]: steps_nodes['step3'] / simulations,
                             time_steps_collect[3]: steps_nodes['step4'] / simulations,
                             time_steps_collect[4]: steps_nodes['step5'] / simulations}
        num_edges[str(p)] = {time_steps_collect[0]: steps_edges['step1'] / simulations,
                             time_steps_collect[1]: steps_edges['step2'] / simulations,
                             time_steps_collect[2]: steps_edges['step3'] / simulations,
                             time_steps_collect[3]: steps_edges['step4'] / simulations,
                             time_steps_collect[4]: steps_edges['step5'] / simulations}
        if p == .8:
            degree_dist_dict = [x/float(simulations) for x in degree_sum_dist]  # get average of the simulations
    return num_nodes, num_edges, degree_dist_dict


#### Expected Values ####
def calc_pref_death(node, G):
    nodes = G.number_of_nodes()
    d_node = G.degree(node)
    d_network = 2.0 * G.number_of_edges()
    return (nodes - d_node) / (nodes ** 2 - d_network)


def calc_pref_attach(node, G):
    d_node = G.degree(node)
    d_network = 2.0 * G.number_of_edges()
    return d_node / d_network


def expected_nodes(p, q, t):
    return (p - q) * t + 2 * q


def run_expected_nodes(p, time_steps):
    nodes = list()
    for t in range(time_steps):
        nodes.append(expected_nodes(p, 1 - p, t + 1))
    return nodes


def expected_edges(p, q, t):
    # a = (2.0*q)/(p-q)
    e = (p * (p - q)) * t
    # return (1+a)*e
    return e


def run_expected_edges(p, time_steps):
    edges = list()
    for t in range(time_steps):
        edges.append(expected_edges(p, 1 - p, t + 1))
    return edges


def expected_degree_dist(p, k):
    return k ** (-1 - ((2 * p) / (2 * p - 1)))


# main function that plots the figures
def plot_expected(time_steps, sim_dict, p_births, markers, E_func, ylim, time_steps_collect, title):
    """
    Figure 2 passes the 'run_expected_nodes' function for E_func.
    Figure 3 passes the 'run_expected_edges' fuction for E_func.
    :param int time_steps: The number of times to simulate.
    :param dict sim_dict:
    :param tuple p_births: A tuple of "p" probabilities to run.
    :param tuple markers: A tuple of markers to indicate which p.
    :param func E_func: The expected value function used for each time step.
    :param ylim: The maximum value for the y-axis.
    :param time_steps_collect: The time points to collect the number of nodes for plotting.
    :return:
    """
    assert len(p_births) <= len(markers), "Must provide marker types for each probability"
    for idx, (m, p) in enumerate(zip(markers, p_births)):
        if p == .8:
            continue
        assert 0 <= p <= 1, "Probabilities must be in decimal format between 0 and 1"
        plt.plot(range(min(time_steps_collect), time_steps + 1), E_func(p, time_steps)[min(time_steps_collect) - 1:],
                 label="p = {}".format(p))
        for t in time_steps_collect:
            plt.plot(t, sim_dict[str(p)][t], marker=markers[idx], color='black')
    plt.legend()
    plt.ylim(0, ylim)
    plt.xlabel("$t$")
    if "node" in title:
        plt.ylabel("$E[n_t]$")
    else:
        plt.ylabel("$E[N^{1}_{k,t}$")
    plt.savefig(os.path.join(os.getcwd(), title + '.png'))
    plt.show()


def plot_degree_dist(degree_hist):
    """
    Plots the cumulative degree distribution: is the probability that X will take a value less than or equal to x.
    On log-log scale.
    :param degree_hist: The degree distribution calculated for a p=.8 and at the 4000/40000 time step
    :return:
    """
    expected_degree_hist = list()
    x = range(1, len(degree_hist)+1)
    for k in x:
        exp_k = expected_degree_dist(.8, k)
        expected_degree_hist.append(exp_k)
    # Total nodes in each
    total_nodes_expected = np.sum(expected_degree_hist)
    total_nodes_simulation = np.sum(degree_hist)
    # Probability distribution
    expected_degree_hist = [y/float(total_nodes_expected) for y in expected_degree_hist]
    degree_hist = [y/float(total_nodes_simulation) for y in degree_hist]
    cum_sim_values = list()
    cum_exp_values = list()
    for idx, (exp, sum) in enumerate(zip(expected_degree_hist, degree_hist)):
        cum_exp_values.append(np.sum(expected_degree_hist[idx:]))
        cum_sim_values.append(np.sum(degree_hist[idx:]))
    plt.loglog(x, cum_sim_values, 'bs')
    plt.loglog(x, cum_exp_values)
    plt.xlabel("$k$")
    plt.ylabel("$P'(k)$")
    plt.savefig(os.path.join(os.getcwd(), "degree_distribution.png"))
    plt.show()


def cumulative_dist(data, bins=20):
    values, base = np.histogram(data, bins=bins, normed=True)
    return values, base


if __name__ == "__main__":
    # set up params
    np.random.seed(12)
    p_births = [.6, .75, .9, .8]
    markers = ("^", "s", "D", "D")

    # Slower implementation
    # time_steps = 5000
    # t_degree = 4000
    # p_births = [.6, .75, .9, .8]
    # simulations = 30

    # ylim = 4000
    # time_steps_collect = range(1000, 6000, 1000)

    # Faster implementation
    simulations = 10
    ylim = 400
    time_steps = 500
    t_degree = 400
    time_steps_collect = range(100, 600, 100)
    # Run Simulation
    nodes_dict, edges_dict, degree_dist_dict = run_simulation(p_births=p_births, simulations=simulations,
                                                              time_steps=time_steps,
                                                              time_steps_collect=time_steps_collect,
                                                              t_degree=t_degree)

    # Plot expected against simulated
    plot_expected(time_steps, nodes_dict, p_births, markers, E_func=run_expected_nodes, ylim=ylim,
                  time_steps_collect=time_steps_collect, title='expected_nodes')
    plot_expected(time_steps, edges_dict, p_births, markers, E_func=run_expected_edges, ylim=ylim,
                  time_steps_collect=time_steps_collect, title='expected_edges')
    print(degree_dist_dict)
    plot_degree_dist(degree_dist_dict)

