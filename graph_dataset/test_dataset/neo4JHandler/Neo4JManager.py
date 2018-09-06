from graph_dataset.create_dataset.neo4JHandler.Neo4JInstance import Neo4JInstance


class Neo4JManager(Neo4JInstance):
    def __init__(self):
        # get neo4j instance
        Neo4JInstance.__init__(self)
