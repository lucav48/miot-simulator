import time
import datetime
import networkx as nx
import random
from graph_dataset.test_dataset import settings
from networkx.algorithms.community.modularity_max import greedy_modularity_communities
from networkx.algorithms.community.kclique import  k_clique_communities
import community as louvain_community
from matplotlib import colors as mcolors


class Performance:

    def __init__(self):
        self.neo = None
        self.start_time = None
        self.end_time = None
        self.table_communities = {}
        self.profile_instances = None

    def set_neo4j(self, neo4j):
        self.neo = neo4j

    def set_profiles(self, prof):
        self.profile_instances = prof

    def get_network_characteristic(self):
        nodes, transactions, n_relation, n_iarch, n_carch, avg_neighborhood, triangle_count,\
        avg_cluster_cofficient, list_cluster_coefficients, message_list_obj_instances = self.neo.get_network_values()
        print "-" * 100
        print "Network Characteristics"
        print "Nodes: ", nodes, " Relationships among instances: ", n_relation, " (i-arch: " + str(n_iarch) +\
                                                                                " c-arch: " + str(n_carch) + \
                                                                                ") Transactions: ", transactions
        print message_list_obj_instances
        print "Average neighborhood: ", avg_neighborhood, " Average transactions per nodes: ", round(float(transactions)/nodes, 3)
        print "Triangle count: ", triangle_count, " Avg. cluster coefficient: ", avg_cluster_cofficient
        print "Cluster coefficient for communities: ", list_cluster_coefficients
        print "-" * 100

    def get_graph_parameters_and_colors(self, graph, approach_profiles):
        print "-" * 100
        colour_map = []
        if graph.edges:
            # k:11 ---> 2 k:17 ---> 4 k:18 ---> 4
            print "Community algorithms"
            print "Triangles count: ", sum(list(nx.triangles(graph).values()))
            print "Average clustering coefficient: ", nx.average_clustering(graph)
            if settings.SUPERVISED_APPROACH:
                colour_map = ["red"] * len(graph.nodes)
                print "Average density: ", str(nx.density(graph))
                connected_components = nx.connected_components(graph)
                string_component = "Components"
                i = 1
                for component in connected_components:
                    string_component = string_component + "\n n: " + str(i) + " length: " + str(len(component))
                    i += 1
                print string_component
                self.information_flow_comparison(graph, approach_profiles)
            else:
                # k_clique, k_best = self.get_best_k_for_clique(graph)
                greedy = list(greedy_modularity_communities(graph))
                partition = louvain_community.best_partition(graph)

                if greedy:
                    cluster_coefficient_cliques = self.calculate_cluster_coefficient_cliques(greedy, graph)
                    colour_map, string_to_print = self.get_colour_map(greedy, graph)
                    print string_to_print
                    print "Greedy (n_communities=" + str(len(greedy)) + ")"
                    print cluster_coefficient_cliques
                if partition:
                    size = int(len(set(partition.values())))
                    set_partition = [[] for _ in range(size)]
                    for node in partition:
                        set_partition[partition[node]].append(node)
                    cluster_coefficient_cliques = self.calculate_cluster_coefficient_cliques(set_partition, graph)
                    avg_hfindhal = self.hfindhal_index_community(set_partition)
                    print "Louvain (n_communities=" + str(size) + ")"
                    print "Avg. Herfindhal index: ", str(avg_hfindhal)
                    print cluster_coefficient_cliques
                    self.information_flow_comparison(graph, approach_profiles)
        else:
            print "No connections in graph, I can't apply algorithms to it."
        print "-" * 100
        return colour_map

    def hfindhal_index_community(self, communities):
        i = 1
        avg_findhal = 0
        num_community = len(communities)
        for community in communities:
            hfindhal_index = 0
            table_community = {}
            community_nodes = self.get_list_nodes(community)
            n_nodes = float(len(community_nodes))
            for node in community_nodes:
                community_node = self.profile_instances[node]["community"]
                if community_node in table_community:
                    table_community[community_node] = table_community[community_node] + 1
                else:
                    table_community[community_node] = 1
            for n_community in table_community:
                hfindhal_index += pow(table_community[n_community] / n_nodes, 2)
            hfindhal_index = round(hfindhal_index, 3)
            avg_findhal += hfindhal_index
            # print "Community ", str(i), " Hfindhal index: ", str(hfindhal_index)
            i += 1
        avg_findhal = avg_findhal / num_community
        return avg_findhal

    def information_flow_comparison(self, graph, approach_profiles):
        i = 0
        number_hops_original_graph = settings.DEPTH_INFORMATION_FLOW
        neo4j_list_nodes = self.get_list_nodes(graph.nodes)
        while i < settings.NUMBER_EXPERIMENT_INFORMATION_FLOW:
            # get node start thematic_view_start_node includes merged nodes, while neo4j_start_node is the single
            # instance
            thematic_view_start_node, neo4j_start_node = \
                self.split_node_and_get_random_instance(random.choice(list(graph.nodes)))
            # apply bfs at certain distance in neo4j graph and choose an end node
            neo4j_visited_nodes, neo4j_count_nodes, end_node = \
                self.neo.get_node_by_bfs_at_distance(neo4j_start_node, neo4j_list_nodes, number_hops_original_graph)
            # nodes has to share at least one context
            if settings.SUPERVISED_APPROACH:
                source_and_target_context = settings.TOPIC_SUPERVISED_APPROACH
            else:
                source_and_target_context = self.intersect_profiles(neo4j_start_node, end_node)
            if end_node != -1 and source_and_target_context:
                # get end_node in thematic view form (merged node or not)
                thematic_view_end_node = self.get_thematic_view_node(graph.nodes, end_node)
                # apply bfs to thematic view
                thematic_view_node_visited, thematic_view_count, thematic_view_depth = \
                    self.compute_bfs(graph, thematic_view_start_node, thematic_view_end_node)
                # first print
                print "-" * 100
                print "Starting from ", thematic_view_start_node, " targeting ", thematic_view_end_node, "\n",\
                    "\tNeo4J nodes involved: ", str(neo4j_count_nodes), "\n", \
                    "\tThematic view node involved: ", str(thematic_view_count), "\n", \
                    "\tNeo4J depth: ", str(number_hops_original_graph), "\n", \
                    "\tThematic depth: ", str(thematic_view_depth)
                print"\tNeo4J context"
                # for each context common to source and target node, we have to count how many nodes have that
                # context during the path and we have to divide that number for the total of nodes traversed by bfs.
                for context in source_and_target_context:
                    context_coefficient = self.count_nodes_with_that_context(neo4j_visited_nodes, None, context) / \
                                          float(len(neo4j_visited_nodes))
                    print "\tContext involved: ", context, " coefficient: ", str(round(context_coefficient, 3))
                # same thing for graph obtained by
                if len(thematic_view_node_visited) > 0:
                    if not settings.SUPERVISED_APPROACH:
                        print "\tUnsupervised context"
                    else:
                        print "\tSupervised context"
                    for context in source_and_target_context:
                        context_coefficient = self.count_nodes_with_that_context(thematic_view_node_visited,
                                                                                 approach_profiles, context) /\
                                              float(len(thematic_view_node_visited))
                        print "\tContext involved: ", context, " coefficient: ", str(round(context_coefficient, 3))
            i += 1

    def count_nodes_with_that_context(self, nodes, profiles, context):
        count_nodes = 0
        for node in nodes:
            if profiles is None:
                profile_node = self.profile_instances[node]["context"]
            else:
                profile_node = profiles[node]
            if context in profile_node:
                count_nodes += 1
        return count_nodes

    def intersect_profiles(self, node1, node2):
        profile1 = self.profile_instances[node1]["context"]
        profile2 = self.profile_instances[node2]["context"]
        intersect_profile = []
        for key in profile1:
            if key in profile2:
                intersect_profile.append(key)
        return intersect_profile

    def calculate_topics_nodes(self, visited_nodes):
        talked_about = {}
        for neo4j_node in visited_nodes:
            node_context = self.profile_instances[neo4j_node]["context"]
            for single_context in node_context:
                if single_context in talked_about:
                    talked_about[single_context] = talked_about[single_context] + 1
                else:
                    talked_about[single_context] = 1
        sorted_talked_about = sorted([(v, k) for (k, v) in talked_about.items()], reverse=True)
        return sorted_talked_about

    def compute_bfs(self, graph, start_node, end_node):
        depth = 0
        found_depth = False
        count_nodes = 0
        nodes_visited = []
        while not found_depth:
            edges = nx.bfs_edges(graph, source=start_node, depth_limit=depth)
            nodes = [v for u, v in edges]
            nodes_at_this_depth = self.difference_list(nodes, nodes_visited)
            if end_node in nodes:
                found_depth = True
                half_length = len(nodes_at_this_depth) / 2
                count_nodes += half_length
                nodes_visited = nodes_visited + nodes_at_this_depth[:half_length]
            elif depth > 6:
                found_depth = True
                count_nodes = -1
                depth = -1
            else:
                depth += 1
                count_nodes += len(nodes_at_this_depth)
                nodes_visited = nodes_visited + nodes_at_this_depth
        return nodes_visited, count_nodes, depth

    def get_thematic_view_node(self, thematic_view_nodes, neo4j_node):
        for node in thematic_view_nodes:
            if "+" in node:
                splitted_node = node.split("+")
                if neo4j_node in splitted_node:
                    return node
            elif neo4j_node == node:
                return node

    def get_list_nodes(self, list_nodes):
        result_list = []
        for node in list_nodes:
            if "+" in node:
                splitted_node = node.split("+")
                for n in splitted_node:
                    result_list.append(n)
            else:
                result_list.append(node)
        return result_list

    def split_node_and_get_random_instance(self, node_code):
        if "+" in node_code:
            return node_code, random.choice(node_code.split("+"))
        else:
            return node_code, node_code

    def get_best_k_for_clique(self, graph):
        k_clique_result = []
        num_community_higher = 0
        k_best = 0
        for i in range(20, 2, -1):
            k_clique = list(k_clique_communities(graph, i))
            if len(k_clique) > num_community_higher:
                num_community_higher = len(k_clique)
                k_clique_result = k_clique
                k_best = i
        return list(k_clique_result), k_best

    def get_colour_map(self, list_cliques, graph):
        colour_map = []
        color_cliques = []
        string_to_print = ""
        list_colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys()
        for i in range(0, len(list_cliques)):
            color = random.choice(list_colors)
            color_cliques.append(color)
            string_to_print = string_to_print + "Community " + str(i + 1) + ": " + color + "  "
            list_colors.remove(color)
        for node in graph.nodes:
            num_clique = list_cliques.index([x for x in list_cliques if node in x][0])
            colour_map.append(color_cliques[num_clique])
        return colour_map, string_to_print

    def calculate_cluster_coefficient_cliques(self, list_cliques, graph):
        cluster_coefficients_string = ""
        i = 1
        sum_cluster_coefficients = 0.
        sum_density_coefficients = 0.
        for cliques in list_cliques:
            clique_graph = nx.Graph()
            for node in cliques:
                clique_graph.add_node(node)
                node_connections = [(x, y) for (x, y) in graph.edges if node == x or node == y]
                for (nodex, nodey) in node_connections:
                    if nodex != node and nodex in cliques:
                        clique_graph.add_edge(nodex, nodey)
                    elif nodey != node and nodey in cliques:
                        clique_graph.add_edge(nodex, nodey)
            single_cluster_coefficient = round(nx.average_clustering(clique_graph), 3)
            single_density_coefficient = round(nx.density(clique_graph), 3)
            cluster_coefficients_string = cluster_coefficients_string + "Community " + str(i) + \
                                          " Cluster coeff.:" + str(single_cluster_coefficient) + \
                                          "  Density:" + str(single_density_coefficient) + "\n"
            sum_cluster_coefficients += single_cluster_coefficient
            sum_density_coefficients += single_density_coefficient
            i += 1
        avg_cluster_coefficient = round(sum_cluster_coefficients / i, 3)
        avg_density_coefficient = round(sum_density_coefficients / i, 3)
        message = "Avg. cluster coefficient: " + str(avg_cluster_coefficient) + "\n" +\
                  "Avg. density coefficient: " + str(avg_density_coefficient) + "\n" + \
                  cluster_coefficients_string
        return message

    def get_start_time(self):
        self.start_time = time.strftime("%H:%M:%S")
        print "Script started at ", self.start_time

    def get_end_time(self):
        self.end_time = time.strftime("%H:%M:%S")
        diff_time = self.difference_time(self.start_time, self.end_time)
        print "Lasted ", diff_time
        print "Script ended at ", self.end_time
        print "-" * 100

    def difference_time(self, start, end):
        start_dt = datetime.datetime.strptime(start, '%H:%M:%S')
        end_dt = datetime.datetime.strptime(end, '%H:%M:%S')
        diff = (end_dt - start_dt)
        return diff

    def get_table_communities(self, instances, profiles):
        for instance in instances:
            community = profiles[instance]["community"]
            if community in self.table_communities:
                self.table_communities[community] = self.table_communities[community] + 1
            else:
                self.table_communities[community] = 1

    def print_table_communities(self, n_nodes):
        print "Distribution nodes taken by communities"
        print "Community \t Number of nodes"
        herfindhal_index = 0
        for key, value in sorted(self.table_communities.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            print "\t%s \t\t\t %s" % (key, value)
            herfindhal_index += round(pow((float(value) / n_nodes), 2), 3)
        print "Herfindhal index: ", str(herfindhal_index)
        print "-" * 100

    def difference_list(self, l1, l2):
        return list(set(l1) - set(l2))