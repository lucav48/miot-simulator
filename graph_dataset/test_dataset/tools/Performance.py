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

    def set_neo4j(self, neo4j):
        self.neo = neo4j

    def get_network_characteristic(self):
        nodes, transactions, n_relation, n_iarch, n_carch, avg_neighborhood, triangle_count, \
        avg_cluster_cofficient, list_cluster_coefficients = self.neo.get_network_values()
        print "-" * 100
        print "Network Characteristics"
        print "Nodes: ", nodes, " Relationships among instances: ", n_relation, " (i-arch: " + str(n_iarch) +\
                                                                                " c-arch: " + str(n_carch) + \
                                                                                ") Transactions: ", transactions
        print "Average neighborhood: ", avg_neighborhood, " Average transactions per nodes: ", round(float(transactions)/nodes, 3)
        print "Triangle count: ", triangle_count, " Avg. cluster coefficient: ", avg_cluster_cofficient
        print "Cluster coefficient for communities: ", list_cluster_coefficients
        print "-" * 100

    def get_graph_parameters_and_colors(self, graph):
        print "-" * 100
        colour_map = []
        if graph.edges:
            # k:11 ---> 2 k:17 ---> 4 k:18 ---> 4
            print "Community algorithms"
            print "Average clustering coefficient: ", nx.average_clustering(graph)
            print "Triangles count: ", sum(list(nx.triangles(graph).values()))
            if settings.SUPERVISED_APPROACH:
                colour_map = ["red"] * len(graph.nodes)
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
                    print "Louvain (n_communities=" + str(size) + ")"
                    print cluster_coefficient_cliques


        else:
            print "No connections in graph, I can't apply algorithms to it."
        print "-" * 100
        return colour_map

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
        sum_coefficients = 0.
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
            single_coefficient = round(nx.average_clustering(clique_graph), 3)
            cluster_coefficients_string = cluster_coefficients_string + "Community " + str(i) + " " +\
                                   str(single_coefficient) + "  "
            sum_coefficients += single_coefficient
            i += 1
        avg_coefficients = round(sum_coefficients / i, 3)
        complete_message = "Avg. coefficient: " + str(avg_coefficients) + "  " + cluster_coefficients_string
        return complete_message

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

    def print_table_communities(self):
        print "Distribution nodes taken by communities"
        print "Community \t Number of nodes"
        for key, value in sorted(self.table_communities.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            print "\t%s \t\t\t %s" % (key, value)
        print "-" * 100
