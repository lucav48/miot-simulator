import utilities
import settings
from neo4j.v1 import GraphDatabase, basic_auth


class Neo4JManager:

    def __init__(self):
        self.neo4j_create_nodes_query = ""
        self.neo4j_create_connections_query = ""
        self._driver = GraphDatabase.driver(settings.NEO4J_URI,
                                            auth=basic_auth(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))
        self.session = self._driver.session()
        self.session.run(settings.NEO4J_DELETE_NODES)

    def neo4j_create_nodes(self, list_nodes):
        for node in list_nodes:
            query = "CREATE (n:Node {" \
                    + "descriptive:'" + utilities.list_to_string(node[0]) \
                    + "', technical:'" + utilities.list_to_string(node[1]) \
                    + "', travel:' " + node[2] \
                    + "', code:'" + node[3] + "'})"
            self.neo4j_create_nodes_query = self.neo4j_create_nodes_query + "\n" + query
            self.execute_query(query)
        # remove last comma
        self.neo4j_create_nodes_query = self.neo4j_create_nodes_query[:-1]

    def neo4j_create_connection(self, idnode1, idnode2):
        query = "MATCH(a:Node), (b:Node) " \
                + "WHERE a.code = '" + idnode1 + "' AND b.code='" + idnode2 + "' " \
                + "CREATE(a) - [r:" + settings.NEO4J_RELATION_TYPE + "]->(b) " \
                + "RETURN r"
        self.neo4j_create_connections_query = self.neo4j_create_connections_query + "\n" + query
        self.execute_query(query)

    def execute_query(self, query):
        self.session.run(query)
