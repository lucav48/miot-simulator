import time
import datetime


class Performance:

    def __init__(self):
        self.neo = None
        self.start_time = None
        self.end_time = None

    def set_neo4j(self, neo4j):
        self.neo = neo4j

    def get_network_characteristic(self):
        nodes, transactions, n_relation, avg_neighborhood = self.neo.get_network_values()
        print "-" * 100
        print "Network Characteristics"
        print "Nodes: ", nodes, ". Relationships among instances: ", n_relation, ". Transactions: ", transactions
        print "Average neighborhood: ", avg_neighborhood
        print "-" * 100

    def get_coefficient_graph(self, graph):
        # TODO
        print ""

    def get_start_time(self):
        self.start_time = time.strftime("%H:%M:%S")
        print "Script started at ", self.start_time

    def get_end_time(self):
        self.end_time = time.strftime("%H:%M:%S")
        diff_time = self.difference_time(self.start_time, self.end_time)
        print "Lasted ", diff_time
        print "Script ended at ", self.end_time

    def difference_time(self, start, end):
        start_dt = datetime.datetime.strptime(start, '%H:%M:%S')
        end_dt = datetime.datetime.strptime(end, '%H:%M:%S')
        diff = (end_dt - start_dt)
        return diff
