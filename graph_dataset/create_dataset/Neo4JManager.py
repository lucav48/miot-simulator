import utilities
import settings
from neo4j.v1 import GraphDatabase, basic_auth


class Neo4JManager:

    def __init__(self):
        self.neo4j_create_nodes_query = ""
        self.neo4j_create_connections_query = ""
        self.neo4j_create_transactions_query = ""
        self._driver = GraphDatabase.driver(settings.NEO4J_URI,
                                            auth=basic_auth(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))
        self.session = self._driver.session()
        self.session.run(settings.NEO4J_DELETE_NODES)

    def neo4j_create_nodes(self, list_nodes):
        # + "', travel:' " + node.travel_path \
        for node in list_nodes:
            query = "CREATE (n:Node {" \
                    + "descriptive:'" + utilities.list_to_string(node.descriptive) \
                    + "', technical:'" + utilities.list_to_string(node.technical) \
                    + "', code:'" + node.code \
                    + "', transactions: '" + node.transactions + "'})"
            self.neo4j_create_nodes_query = self.neo4j_create_nodes_query + "\n" + query
            self.execute_query(query)
        # remove last comma
        # self.neo4j_create_nodes_query = self.neo4j_create_nodes_query[:-1]

    def neo4j_create_connections(self, conn):
        for pair in conn:
            node, other_node = pair.split("-")
            query = "MATCH(a:Node), (b:Node) " \
                + "WHERE a.code = '" + node + "' AND b.code='" + other_node + "' " \
                + "CREATE UNIQUE (a) - [r:" + settings.NEO4J_RELATION_TYPE + "]->(b) " \
                + "RETURN r"
            self.neo4j_create_connections_query = self.neo4j_create_connections_query + "\n" + query
            self.execute_query(query)
        # remove last comma
        # self.neo4j_create_nodes_query = self.neo4j_create_nodes_query[:-1]

    def check_if_nodes_connected(self, idnode1, idnode2):
        query = "MATCH (a:Node), (b:Node) " \
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
            transaction_string = "'" + transaction.source + "," + \
                                 transaction.destination + "," + \
                                 transaction.timestamp + "," + \
                                 transaction.context + "," + \
                                 transaction.message + "'"
            query = "MATCH (n:Node) " \
                    + "WHERE n.code='" + transaction.source + "'" \
                    + "SET n.transactions = n.transactions + [" + transaction_string + "]"
            self.neo4j_create_transactions_query = self.neo4j_create_transactions_query + "\n" + query
            self.execute_query(query)
        # remove last comma
        # self.neo4j_create_nodes_query = self.neo4j_create_nodes_query[:-1]

    def execute_query(self, query):
        return self.session.run(query)
