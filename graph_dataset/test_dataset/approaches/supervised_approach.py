from graph_dataset.test_dataset.tools import utilities
from graph_dataset.test_dataset import settings
import networkx as nx
import matplotlib.pyplot as plt


def start(profiles, neo, performance):
    print("Supervised approach started!")
    q_first = utilities.define_q_first()
    ci = build_ci(profiles.p_content_single_instance, q_first)
    ri = build_ri(ci, q_first)
    print "Topic requested: ", ', '.join(settings.TOPIC_SUPERVISED_APPROACH)
    print "Threshold to filter instances: ", str(settings.THRESHOLD_SUPERVISED)
    print "Recall supervised Candidate instances: ", len(ci), " Filtered instances: ", len(ri)
    performance.get_table_communities(ri, profiles.p_content_single_instance)
    refactor_ri, ri_connections = build_connections(ri, neo, profiles.p_content_single_instance)
    print "There are ", len(refactor_ri), " compatible to user's query."
    graph = build_graph_networkx(refactor_ri, ri_connections)
    print "Thematic view has: ", graph.number_of_nodes(), " nodes and ", graph.number_of_edges(), " edges."
    colour_map = performance.get_graph_parameters_and_colors(graph, refactor_ri)
    performance.print_table_communities(len(graph.nodes))
    performance.get_end_time()
    # print_graph(graph, colour_map)
    return graph


def build_connections(nodes, neo, profile_instances):
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
    new_nodes, connections = fuse_node(nodes, fusing_nodes, connections, profile_instances)
    return new_nodes, connections


def fuse_node(nodes, f_nodes, conn, profile_instances):
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
    # print number of nodes fused
    print "-" * 100
    cont = len(fusing_nodes_complete)
    print "Details on C-nodes fused community"
    for node in fusing_nodes_complete:
        community = {}
        community[profile_instances[node]["community"]] = 1
        for list_node in fusing_nodes_complete[node]:
            node_community = profile_instances[list_node]["community"]
            if node_community in community:
                community[node_community] = community[node_community] + 1
            else:
                community[node_community] = 1
        print "Node: ", node, " ", community.items()
        cont += len(fusing_nodes_complete[node])
    print "Number of c-nodes fused: ", cont
    return nodes, conn


def update_connections(conn, node1, node2):
    delete_list = []
    for i in range(0, len(conn)):
        fused = node1 + "+" + node2
        n1, n2 = conn[i].split("-")
        if (n1 == node1 and n2 == node2) or (n2 == node1 and n1 == node2):
            delete_list.append(conn[i])
        elif n1 == node1:
            conn[i] = fused + "-" + n2
        elif n2 == node1:
            conn[i] = fused + "-" + n1
        elif n1 == node2:
            conn[i] = fused + "-" + n2
        elif n2 == node2:
            conn[i] = fused + "-" + n1
    for d in delete_list:
        conn.remove(d)
    return list(set(conn))


def build_graph_networkx(nodes, connections):
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node)
    for connection in connections:
        links = connection.split("-")
        graph.add_edge(links[0], links[1], cross_node="")
    if connections:
        graph = check_if_graph_connected(graph)
    return graph


def check_if_graph_connected(graph):
    if nx.is_connected(graph):
        print "Graph connected."
        return graph
    else:
        print "Graph not connected. It needs more edges to be connected."
        if settings.ADD_EDGES_THROUGH_DFS:
            graph = utilities.add_edges_dfs(graph)
        if settings.ADD_MORE_EDGES:
            graph = utilities.add_edges_isolated_nodes(graph, nx)
        return graph


def print_graph(graph, colour_map):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_color=colour_map, with_labels=True)
    edge_labels = nx.get_edge_attributes(graph, 'cross_node')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    if graph.nodes:
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
