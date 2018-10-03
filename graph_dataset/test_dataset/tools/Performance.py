import time
import datetime
import networkx as nx
import random
from networkx.algorithms import community
from graph_dataset.test_dataset import settings
from networkx.algorithms.community.modularity_max import greedy_modularity_communities


class Performance:

    def __init__(self):
        self.neo = None
        self.start_time = None
        self.end_time = None
        self.approach = None

    def set_neo4j(self, neo4j):
        self.neo = neo4j

    def get_network_characteristic(self):
        nodes, transactions, n_relation, avg_neighborhood, triangle_count, \
        avg_cluster_cofficient, list_cluster_coefficients = self.neo.get_network_values()
        print "-" * 100
        print "Network Characteristics"
        print "Nodes: ", nodes, " Relationships among instances: ", n_relation, " Transactions: ", transactions
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

            k_clique, k_best = self.get_best_k_for_clique(graph)
            greedy = list(greedy_modularity_communities(graph))
            cluster_coefficient_cliques = self.calculate_cluster_coefficient_cliques(greedy, graph)
            colour_map, string_to_print = self.get_colour_map(greedy, graph)
            print "Greedy (n_communities=" + str(len(greedy)) + ")"
            print "Cluster coefficient Greedy : ", cluster_coefficient_cliques
            print string_to_print
            print "K-Clique (K=" + str(k_best) + ", n_communities=" + str(len(k_clique)) + ")"
            print "Cluster coefficient K-Clique: ", self.calculate_cluster_coefficient_cliques(k_clique, graph)
        else:
            print "No connections in graph, I can't apply algorithms to it."
        print "-" * 100
        return colour_map

    def get_best_k_for_clique(self, graph):
        k_clique_result = None
        num_community_higher = 0
        k_best = 0
        for i in range(20, 2, -1):
            k_clique = list(community.k_clique_communities(graph, i))
            if len(k_clique) > num_community_higher:
                num_community_higher = len(k_clique)
                k_clique_result = k_clique
                k_best = i
        return k_clique_result, k_best

    def get_colour_map(self, list_cliques, graph):
        colour_map = []
        color_cliques = []
        list_colors = settings.COLORS
        string_to_print = ""
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
        cluster_coefficients = ""
        i = 1
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
            cluster_coefficients = cluster_coefficients + "Community " + str(i) + " " +\
                                   str(round(nx.average_clustering(clique_graph), 3)) + "  "
            i += 1
        return cluster_coefficients

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
