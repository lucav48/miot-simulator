from graph_dataset.create_dataset.neo4JHandler import credentials
from neo4j.v1 import GraphDatabase, basic_auth


class Neo4JInstance:
    def __init__(self):
        # get instance of graph db
        self._driver = GraphDatabase.driver(credentials.NEO4J_URI,
                                            auth=basic_auth(credentials.NEO4J_USERNAME,
                                                            credentials.NEO4J_PASSWORD))
        self.session = self._driver.session()
