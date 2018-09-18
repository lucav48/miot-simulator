from graph_dataset.test_dataset import settings as settings
import random
import time
import datetime


def u_plus_operator(items):
    counting_list = {}
    for item in items:
        if item in counting_list:
            counting_list[item] += 1
        else:
            counting_list[item] = 1
    return counting_list


def sum_occurrences_dict(list1, list2):
    results = {}
    for key in list1:
        results[key] = list1[key]
        if key in list2:
            results[key] = int(list1[key]) + int(list2[key])
    for key in list2:
        if key not in results:
            results[key] = list2[key]
    return results


def define_q_first():
    q_first = {}
    for key in settings.TOPIC_SUPERVISED_APPROACH:
        q_first[key] = 1
    return q_first


def sum_occurrences(list_to_sum):
    sum_list = 0
    for key in list_to_sum:
        sum_list += float(list_to_sum[key])
    return sum_list


def intersect_dict(dict1, dict2):
    result_dict = {}
    for key in dict1:
        if key in dict2:
            result_dict[key] = float(dict1[key]) + float(dict2[key])
    return result_dict


def jaccard_star(topicset1, topicset2):
    common_ts = intersect_dict(topicset1, topicset2)
    num = sum_occurrences(common_ts)
    den = (sum_occurrences(topicset1) + sum_occurrences(topicset2))
    tot = num / den
    return tot


def subset(list1, list2):
    for x in list1:
        if x in list2:
            return True
    return False


def add_edges(g):
    no_comp = 0
    comp = {}
    vis = {}
    size_comp = {}
    edges = {}
    for node in g.nodes:
        edges[node] = {}
        comp[node] = {}
        vis[node] = 0
        size_comp[node] = node
        for other_node in g.nodes:
            if node != other_node:
                if other_node not in edges:
                    edges[other_node] = {}
                    comp[other_node] = {}
                if (node, other_node) in g.edges or (other_node, node) in g.edges:
                    edges[node][other_node] = 1
                    edges[other_node][node] = 1
                else:
                    edges[node][other_node] = 0
                    edges[other_node][node] = 0
                comp[node][other_node] = 0
    for i in g.nodes:
        if vis[i] == 0:
            dfs(i, vis, comp, no_comp, size_comp, g.nodes, edges)
            no_comp += 1
    for key1 in comp:
        for key2 in comp[key1]:
            if comp[key1][key2] != 0:
                g.add_edge(key1, key2, cross_node="X")
                print "Added ", key1, "   ", key2
    return g


def dfs(start, vis, comp, no_comp, size_comp, nodes, edges):
    vis[start] = 1
    comp[nodes.keys()[no_comp]][size_comp[nodes.keys()[no_comp + 1]]] = start
    for i in nodes:
        if vis[i] == 1 or edges[start][i] == 0:
            continue
        dfs(i, vis, comp, no_comp, size_comp, nodes, edges)


def add_edges_isolated_nodes(g, nx):
    node_isolated = list(nx.isolates(g))
    not_isolated = [x for x in g.nodes if x not in node_isolated]
    for isolated in node_isolated:
        other_node = random.choice(not_isolated)
        g.add_edge(isolated, other_node, cross_node="X")
    return g


def has_partial_key(keys, partial_key):
    result_key = None
    for composite_key in keys:
        key_list = composite_key.split("+")
        if partial_key in key_list:
            result_key = composite_key
    return result_key


def find_over_connection(list1, composite_key):
    keys = composite_key.split("+")
    connection = []
    for key in keys:
        if key in list1:
            connection.append(key)
    return connection
