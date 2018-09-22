import graph_dataset.create_dataset.settings as settings
from graph_dataset.create_dataset.tools import utilities
from Neo4JInstance import Neo4JInstance


class Neo4JManager(Neo4JInstance):

    def __init__(self):
        # get neo4j instance
        Neo4JInstance.__init__(self)
        # query to write to file
        self.neo4j_create_nodes_query = []
        self.neo4j_create_instances_query = []
        self.neo4j_create_connections_query = []
        self.neo4j_create_transactions_query = []
        self.neo4j_adjust_communities_query = ""
        self.neo4j_delete_isolated_nodes_query = ""
        # load settings
        self.object_label = settings.NEO4J_OBJECT_LABEL
        self.instance_label = settings.NEO4J_INSTANCE_LABEL
        self.transaction_label = settings.NEO4J_TRANSACTION_LABEL
        self.relation_between_instances_label = settings.NEO4J_RELATION_INSTANCE_TYPE
        self.relation_object_instance_label = settings.NEO4J_RELATION_OBJECT_INSTANCE_TYPE
        self.relation_transaction_label = settings.NEO4J_RELATION_TRANSACTION_TYPE
        # clear all previously nodes and relationship
        self.execute_query(settings.NEO4J_DELETE_NODES)

    def neo4j_create_objects(self, list_object):
        # + "', travel:' " + node.travel_path \
        for one_object in list_object:
            query = "CREATE (n:" + self.object_label + " {" + one_object.object_as_string() + "})"
            self.neo4j_create_nodes_query.append(query)

    def create_query_connection(self, instance1, instance2):
        query = "MATCH(a:" + self.instance_label + "), (b:" + self.instance_label + ") " \
                + "WHERE a.code = '" + instance1 + "' AND b.code='" + instance2 + "' " \
                + "MERGE (a) - [:" + self.relation_between_instances_label + "]->(b)"
        return query

    def neo4j_add_transactions(self, transaction_list):
        for transaction in transaction_list:
            # create transaction node
            query = "CREATE (t:" + self.transaction_label + " {" + transaction.transaction_as_string() + "})"
            self.neo4j_create_transactions_query.append(query)
            # create transaction relation between instances
            query = "MATCH(a:" + self.instance_label + "), (b:" + self.instance_label + ")," \
                    "(t:" + self.transaction_label + ") " \
                    + "WHERE a.code = '" + transaction.source + "' AND b.code='" + transaction.destination + "' " \
                    + "AND t.code = '" + transaction.code + "' " \
                    + "CREATE UNIQUE (a) - [:" + self.relation_transaction_label + "]->(t) " \
                    + "CREATE UNIQUE (t) - [:" + self.relation_transaction_label + "]->(b) "
            self.neo4j_create_transactions_query.append(query)

    def neo4j_create_objects_instances(self, objects):
        for one_object in objects:
            for instance in one_object.instances:
                query = "MATCH(n:" + self.object_label + ") " \
                        + "WHERE n.code = '" + one_object.code + "' " \
                        + "CREATE (i:" + self.instance_label + " {" + instance.instance_as_string() + "}) " \
                        + "MERGE (n) - [:" + self.relation_object_instance_label + "]->(i) "
                self.neo4j_create_instances_query.append(query)

    def neo4j_delete_isolated_nodes(self):
        query = "MATCH(n:Instance) WHERE not (n)-[:"\
                + self.relation_between_instances_label + "]-() DETACH DELETE  n"
        self.neo4j_delete_isolated_nodes_query = query

    def adjust_communities(self):
        list_communities = [x for x in range(1, settings.NUMBER_OF_COMMUNITIES + 1)]
        query = "UNWIND " + utilities.list_to_string(list_communities, ",") + " AS comm "\
                "WITH comm"\
                "MATCH(n:Instance) WHERE n.community = comm "\
                "WITH n, comm " \
                "OPTIONAL MATCH (n)-[r:LINKED]-(n2:Instance) WHERE n2.community = comm "\
                "WITH n, n2 WHERE n2 is null "\
                "WITH collect(n.code) as nodes "\
                "UNWIND nodes as single_node "\
                "MATCH(n3:Instance)-[:LINKED]-(n4:Instance) "\
                "WHERE n3.code = single_node "\
                "WITH single_node, n4.community as comm, count(n4.community) as listone "\
                "WITH single_node, collect({community: comm, value:listone}) as biglistone "\
                "UNWIND biglistone as element "\
                "WITH single_node,MAX(element.value) as result, biglistone "\
                "WITH single_node, result, filter(element in biglistone WHERE element.value = result) as the_one "\
                "MATCH(n:Instance) WHERE n.code = single_node SET n.community = the_one[0].community "
        self.neo4j_adjust_communities_query = query

