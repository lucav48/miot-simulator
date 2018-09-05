import graph_dataset.create_dataset.tools.utilities as utilities
import graph_dataset.create_dataset.settings as settings
from neo4j.v1 import GraphDatabase, basic_auth


class Neo4JManager:

    def __init__(self):
        # query to write to file
        self.neo4j_create_nodes_query = ""
        self.neo4j_create_instances_query = ""
        self.neo4j_create_connections_query = ""
        self.neo4j_create_transactions_query = ""
        # load settings
        self.object_label = settings.NEO4J_OBJECT_LABEL
        self.instance_label = settings.NEO4J_INSTANCE_LABEL
        self.transaction_label = settings.NEO4J_TRANSACTION_LABEL
        self.relation_between_instances_label = settings.NEO4J_RELATION_INSTANCE_TYPE
        self.relation_object_instance_label = settings.NEO4J_RELATION_OBJECT_INSTANCE_TYPE
        self.relation_transaction_label = settings.NEO4J_RELATION_TRANSACTION_TYPE
        # get instance of graph db
        self._driver = GraphDatabase.driver(settings.NEO4J_URI,
                                            auth=basic_auth(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))
        self.session = self._driver.session()
        # clear all previously nodes and relationship
        self.session.run(settings.NEO4J_DELETE_NODES)

    def neo4j_create_objects(self, list_object):
        # + "', travel:' " + node.travel_path \
        for one_object in list_object:
            query = "CREATE (n:" + self.object_label + " {" \
                    + "descriptive:'" + utilities.list_to_string(one_object.descriptive) \
                    + "', technical:'" + utilities.list_to_string(one_object.technical) \
                    + "', code:'" + one_object.code + "'})"
            self.neo4j_create_nodes_query = self.neo4j_create_nodes_query + "\n" + query + ";"
            self.execute_query(query)

    def neo4j_create_connections(self, conn):
        for pair in conn:
            instance, other_instance = pair.split("-")
            query = "MATCH(a:" + self.instance_label + "), (b:" + self.instance_label + ") " \
                    + "WHERE a.code = '" + instance + "' AND b.code='" + other_instance + "' " \
                    + "CREATE UNIQUE (a) - [r:" + self.relation_between_instances_label + "]->(b) " \
                    + "RETURN r"
            self.neo4j_create_connections_query = self.neo4j_create_connections_query + "\n" + query + ";"
            self.execute_query(query)

    def check_if_instances_connected(self, idinstance1, idinstance2):
        query = "MATCH (a:" + self.instance_label + "), (b:" + self.instance_label + ") " \
                + "WHERE a.code = '" + idinstance1 + "' AND b.code='" + idinstance2 + "' " \
                + "AND (a)-[:" + self.relation_between_instances_label + "*]-(b) " \
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
            # create transaction relation between instances
            query = "MATCH(a:" + self.instance_label + "), (b:" + self.instance_label + ")," \
                    "(t:" + self.transaction_label + ") " \
                    + "WHERE a.code = '" + transaction.source + "' AND b.code='" + transaction.destination + "' " \
                    + "AND ID(t) = " + transaction_id + " " \
                    + "CREATE UNIQUE (a) - [r1:" + self.relation_transaction_label + "]->(t) " \
                    + "CREATE UNIQUE (t) - [r2:" + self.relation_transaction_label + "]->(b) " \
                    + "RETURN r1,r2"
            self.neo4j_create_transactions_query = self.neo4j_create_transactions_query + "\n" + query + ";"
            self.execute_query(query)

    def neo4j_retrieve_connected_instances(self, instance_code):
        result = []
        query = "MATCH (a:" + self.instance_label + "), (b:" + self.instance_label + ") " \
                + "WHERE a.code = '" + instance_code + "'" \
                + "AND (a)-[:" + self.relation_between_instances_label + "]-(b) " \
                + "RETURN b.code LIMIT 50"
        query_result = self.execute_query(query)
        for x in query_result:
            result.append(x["b.code"])
        return result

    def execute_query(self, query):
        return self.session.run(query)

    def neo4j_create_objects_instances(self, objects):
        for one_object in objects:
            for instance in one_object.instances:
                query = "MATCH(n:" + self.object_label + ") " \
                        + "WHERE n.code = '" + one_object.code + "' " \
                        + "CREATE (i:" + self.instance_label + " {code:'" + instance.code + "'," \
                                                                "community:'" + instance.community + "'}) " \
                        + "CREATE UNIQUE (n) - [r:" + self.relation_object_instance_label + "]->(i) " \
                        + "RETURN r"
                self.neo4j_create_instances_query = self.neo4j_create_instances_query + "\n" + query + ";"
                self.execute_query(query)
