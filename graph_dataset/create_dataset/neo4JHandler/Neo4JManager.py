import graph_dataset.create_dataset.tools.utilities
import graph_dataset.create_dataset.settings
from neo4j.v1 import GraphDatabase, basic_auth


class Neo4JManager:

    def __init__(self):
        self.neo4j_create_nodes_query = ""
        self.neo4j_create_connections_query = ""
        self.neo4j_create_transactions_query = ""
        # load settings
        self.node_label = graph_dataset.create_dataset.settings.NEO4J_NODE_LABEL
        self.transaction_label = graph_dataset.create_dataset.settings.NEO4J_TRANSACTION_LABEL
        self.relation_node_label = graph_dataset.create_dataset.settings.NEO4J_RELATION_NODE_TYPE
        self.relation_transaction_label = graph_dataset.create_dataset.settings.NEO4J_TRANSACTION_NODE_TYPE
        # get instance of graph db
        self._driver = GraphDatabase.driver(graph_dataset.create_dataset.settings.NEO4J_URI,
                                            auth=basic_auth(graph_dataset.create_dataset.settings.NEO4J_USERNAME, graph_dataset.create_dataset.settings.NEO4J_PASSWORD))
        self.session = self._driver.session()
        # clear all previously nodes and relationship
        self.session.run(graph_dataset.create_dataset.settings.NEO4J_DELETE_NODES)

    def neo4j_create_nodes(self, list_nodes):
        # + "', travel:' " + node.travel_path \
        for node in list_nodes:
            query = "CREATE (n:" + self.node_label + " {" \
                    + "descriptive:'" + graph_dataset.create_dataset.tools.utilities.list_to_string(node.descriptive) \
                    + "', technical:'" + graph_dataset.create_dataset.tools.utilities.list_to_string(node.technical) \
                    + "', code:'" + node.code + "'})"
            self.neo4j_create_nodes_query = self.neo4j_create_nodes_query + "\n" + query + ";"
            self.execute_query(query)

    def neo4j_create_connections(self, conn):
        for pair in conn:
            node, other_node = pair.split("-")
            query = "MATCH(a:" + self.node_label + "), (b:" + self.node_label + ") " \
                + "WHERE a.code = '" + node + "' AND b.code='" + other_node + "' " \
                + "CREATE UNIQUE (a) - [r:" + self.relation_node_label + "]->(b) " \
                + "RETURN r"
            self.neo4j_create_connections_query = self.neo4j_create_connections_query + "\n" + query + ";"
            self.execute_query(query)

    def check_if_nodes_connected(self, idnode1, idnode2):
        query = "MATCH (a:" + self.node_label + "), (b:" + self.node_label + ") " \
                + "WHERE a.code = '" + idnode1 + "' AND b.code='" + idnode2 + "' " \
                + "AND (a)-[*]-(b) " \
                + "RETURN a.code,b.code"
        query_result = self.execute_query(query)
        result = ""
        for x in query_result:
            result = x["a.code"] + "-" + x["b.code"]
        return result

    def neo4j_add_transactions(self, transaction_list):
        for transaction in transaction_list:
            # create transaction node
            query = "CREATE (t:" + self.transaction_label + " {" \
                    + "timestamp:'" + transaction.timestamp \
                    + "', context:'" + transaction.context \
                    + "', message: '" + transaction.message + "'}) " \
                    + "RETURN Id(t)"
            self.neo4j_create_transactions_query = self.neo4j_create_transactions_query + "\n" + query + ";"
            query_result = self.execute_query(query)
            transaction_id = str([x["Id(t)"] for x in query_result][0])
            # create transaction relation between nodes
            query = "MATCH(a:" + self.node_label + "), (b:" + self.node_label + ")," \
                    "(t:" + self.transaction_label + ") " \
                    + "WHERE a.code = '" + transaction.source + "' AND b.code='" + transaction.destination + "' " \
                    + "AND ID(t) = " + transaction_id + " " \
                    + "CREATE UNIQUE (a) - [r1:" + self.relation_transaction_label + "]->(t) " \
                    + "CREATE UNIQUE (t) - [r2:" + self.relation_transaction_label + "]->(b) " \
                    + "RETURN r1,r2"
            self.neo4j_create_transactions_query = self.neo4j_create_transactions_query + "\n" + query + ";"
            self.execute_query(query)

    def neo4j_retrieve_connected_node(self, node_code):
        result = []
        query = "MATCH (a:" + self.node_label + "), (b:" + self.node_label + ") " \
                + "WHERE a.code = '" + node_code + "'" \
                + "AND (a)-[:" + self.relation_node_label + "]-(b) " \
                + "RETURN b.code"
        query_result = self.execute_query(query)
        for x in query_result:
            result.append(x["b.code"])
        return result

    def execute_query(self, query):
        return self.session.run(query)
