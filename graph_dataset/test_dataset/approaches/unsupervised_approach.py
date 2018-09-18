from graph_dataset.test_dataset.tools import utilities
from graph_dataset.test_dataset import settings
import networkx as nx
import matplotlib.pyplot as plt


def start(profiles, neo):
    print("Unsupervised approach started!")
    instances_to_merge = neo.get_instances_to_merge_unsupervised()
    unsupervised_instances, instances_merged = merge_instances(instances_to_merge,
                                                               profiles.p_content_single_instance)
    connections = neo.get_instances_connections()
    merged_connections = merge_connections(connections, unsupervised_instances)
    fill_unsupervised_instances(unsupervised_instances, instances_merged, profiles.p_content_single_instance)
    graph = build_graph(unsupervised_instances, merged_connections, profiles.p_content_single_instance)
    print_graph(graph)
    return graph


def build_graph(instances, connections, p_single_instance):
    graph = nx.Graph()
    for node in connections:
        graph.add_node(node)
        for conn in connections[node]:
            if conn in instances:
                j_star = utilities.jaccard_star(instances[node][settings.TRANSACTION_CONTEXT_FIELD],
                                                instances[conn][settings.TRANSACTION_CONTEXT_FIELD])
                j_star = round(j_star, 2)
                graph.add_edge(node, conn, j_star=j_star)
            else:
                complete_connection = utilities.has_partial_key(instances.keys(), conn)
                if complete_connection:
                    over_connection = utilities.find_over_connection(connections[node], complete_connection)
                    if len(over_connection) > 1:
                        j_stars = []
                        for connection in over_connection:
                            j_stars.append(utilities.jaccard_star(instances[node][settings.TRANSACTION_CONTEXT_FIELD],
                                                                  p_single_instance[connection][settings.TRANSACTION_CONTEXT_FIELD]))
                        j_star = min(1, (max(j_stars) + settings.ALPHA_COEFFICIENT*sum(j_stars)))
                    else:
                        j_star = utilities.jaccard_star(instances[node][settings.TRANSACTION_CONTEXT_FIELD],
                                                        instances[complete_connection][settings.TRANSACTION_CONTEXT_FIELD])
                    j_star = round(j_star, 2)
                    graph.add_edge(node, complete_connection, j_star=j_star)
    print "Thematic view has: ", graph.number_of_nodes(), " nodes and ", graph.number_of_edges(), " edges."
    return graph


def print_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(graph, 'j_star')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.show()


def fill_unsupervised_instances(unsupervised_instances, instances_merged, p_single_instance):
    for instance in p_single_instance:
        if instance not in instances_merged:
            unsupervised_instances[instance] = {}
            unsupervised_instances[instance] = p_single_instance[instance]


def merge_connections(connections, unsupervised_instances):
    merged_connections = {}
    for node in unsupervised_instances:
        all_nodes = node.split("+")
        new_connections = []
        for n in all_nodes:
            for conn in connections[n]:
                if conn not in new_connections:
                    new_connections.append(conn)
            del connections[n]
        merged_connections[node] = new_connections
    for node in connections:
        merged_connections[node] = {}
        merged_connections[node] = connections[node]
    return merged_connections


def merge_instances(instances_to_merge, p_single_instance):
    merged_instances = {}
    instances = []
    for in_to_merge in instances_to_merge:
        new_code = in_to_merge
        new_profile = {}
        for related_instance in instances_to_merge[in_to_merge]:
            if related_instance not in instances:
                new_code = new_code + "+" + related_instance
                for prop in settings.PROPERTY_TRANSACTION_TO_WATCH:
                    if prop not in new_profile:
                        new_profile[prop] = {}
                    new_profile[prop] = utilities.sum_occurrences_dict(new_profile[prop],
                                                                       p_single_instance[related_instance][prop])
                instances.append(related_instance)
        if in_to_merge not in instances:
            instances.append(in_to_merge)
            merged_instances[new_code] = new_profile
    return merged_instances, instances
