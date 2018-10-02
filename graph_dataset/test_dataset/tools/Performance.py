import time
import datetime
import networkx as nx


class Performance:

    def __init__(self):
        self.neo = None
        self.start_time = None
        self.end_time = None

    def set_neo4j(self, neo4j):
        self.neo = neo4j

    def get_network_characteristic(self):
        nodes, transactions, n_relation, avg_neighborhood, triangle_count, \
        avg_cluster_cofficient, list_cluster_coefficients = self.neo.get_network_values()
        print "-" * 100
        print "Network Characteristics"
        print "Nodes: ", nodes, ". Relationships among instances: ", n_relation, ". Transactions: ", transactions
        print "Average neighborhood: ", avg_neighborhood, " Average transactions per nodes: ", round(float(transactions)/nodes, 3)
        print "Triangle count: ", triangle_count, " Avg. cluster coefficient: ", avg_cluster_cofficient
        print "Cluster coefficient for communities: ", list_cluster_coefficients
        print "-" * 100

    def get_graph_parameters(self, graph):
        print "-" * 100
        if graph.edges:
            print "Community algorithms"
            print "Average clustering coefficient: ", nx.average_clustering(graph)
            print "Triangles count: ", sum(list(nx.triangles(graph).values()))
            # print "Label propagation: ", list(community.label_propagation_communities(graph))
            # print "K-Clique: ", list(community.k_clique_communities(graph, 3))
            # print "Connectivity algorithms"
            # k_edge = 3
            # print "K-edge (k=" + str(k_edge) + "): ", sorted(map(sorted, nx.k_edge_components(graph, k=k_edge)))
            # print "K-components: ", nx.k_components(graph)
        else:
            print "No connections in graph, I can't apply algorithms to it."
        print "-" * 100

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
