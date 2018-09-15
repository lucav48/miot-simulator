from graph_dataset.test_dataset.tools import utilities
from graph_dataset.test_dataset import settings
import networkx as nx
import matplotlib.pyplot as plt


def start(profiles, neo):
    print("Supervised approach started!")
    q_first = utilities.define_q_first()
    ci = build_ci(profiles.p_content_single_instance, q_first)
    ri = build_ri(ci, q_first)
    refactor_ri, ri_connections = build_connections(ri, neo)
    build_graph_networkx(refactor_ri, ri_connections)
    print "There are ", len(ri), " compatible to user's query."


def build_connections(nodes, neo):
    connections = []
    fusing_nodes = {}
    for node in nodes:
        fusing_nodes[node] = []
        neighborhood = neo.get_communities_neighborhood(node)
        for neighbor in neighborhood:
            if neighbor in nodes:
                if neighborhood[neighbor]:
                    # build a link between that node (inner arc)
                    connections.append(node + "-" + neighbor)
                else:
                    fusing_nodes[node].append(neighbor)
                    connections.append(node + "-" + neighbor)
        if not fusing_nodes[node]:
            del fusing_nodes[node]
    nodes, connections = fuse_node(nodes, fusing_nodes, connections)
    return nodes, connections


def fuse_node(nodes, f_nodes, conn):
    # now i fuse nodes
    for node in f_nodes:
        if f_nodes[node]:
            for other_node in f_nodes:
                if node != other_node and f_nodes[other_node]:
                    if utilities.subset(f_nodes[node] + [node], f_nodes[other_node] + [other_node]):
                        new_node_list = list(set(f_nodes[node] + f_nodes[other_node] + [other_node]))
                        f_nodes[node] = new_node_list
                        f_nodes[other_node] = []
    fusing_nodes_complete = {}
    for node in f_nodes:
        if f_nodes[node]:
            if node in f_nodes[node]:
                f_nodes[node].remove(node)
            fusing_nodes_complete[node] = f_nodes[node]
    for node in fusing_nodes_complete:
        new_node = node
        new_profile = nodes[node]
        for node_to_fuse in fusing_nodes_complete[node]:
            conn = update_connections(conn, new_node, node_to_fuse)
            new_node = new_node + "+" + node_to_fuse
            new_profile = utilities.sum_occurrences_dict(new_profile, nodes[node_to_fuse])
            del nodes[node_to_fuse]
        del nodes[node]
        nodes[new_node] = new_profile
    return nodes, conn


def update_connections(conn, node1, node2):
    delete_list = []
    for i in range(0, len(conn)):
        fused = node1 + "+" + node2
        n1, n2 = conn[i].split("-")
        if (n1 == node1 and n2 == node2) or (n2 == node1 and n1 == node2):
            delete_list.append(i)
        elif n1 == node1:
            conn[i] = fused + "-" + n2
        elif n2 == node1:
            conn[i] = fused + "-" + n1
        elif n1 == node2:
            conn[i] = fused + "-" + n2
        elif n2 == node2:
            conn[i] = fused + "-" + n1
    for d in delete_list:
        del conn[d]
    return list(set(conn))


def build_graph_networkx(nodes, connections):
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node)
    for connection in connections:
        links = connection.split("-")
        graph.add_edge(links[0], links[1], cross_node="")
    graph = check_if_graph_connected(graph)
    print_graph(graph)


def check_if_graph_connected(graph):
    if nx.is_connected(graph):
        print "Graph connected."
        return graph
    else:
        print "Graph not connected. It needs more edges to be connected."
        graph = utilities.add_edges_isolated_nodes(graph, nx)
        graph = utilities.add_edges(graph)
        return graph


def print_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(graph, 'cross_node')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.show()


def build_ri(ci, q_first):
    ri = {}
    for instance in ci:
        j_star = utilities.jaccard_star(ci[instance], q_first)
        if j_star > settings.THRESHOLD_SUPERVISED:
            ri[instance] = ci[instance]
    return ri


def build_ci(instances, q_first):
    ci = {}
    con = settings.TRANSACTION_CONTEXT_FIELD
    for supervised_key in q_first:
        for instance in instances:
            if supervised_key in instances[instance][con]:
                ci[instance] = instances[instance][con]
    return ci
