from graph_dataset.create_dataset.neo4JHandler.Neo4JInstance import Neo4JInstance
from graph_dataset.trust_and_reputation import settings
import neo4JQuery
import random
from neo4jObject import TrustedInstance
from neo4jObject import TrustedTransaction


class Neo4JManager(Neo4JInstance):
    def __init__(self):
        # get neo4j instance
        Neo4JInstance.__init__(self)
        self.number_of_instances = self.get_network_parameter(neo4JQuery.NUMBER_OF_INSTANCE)
        self.number_of_i_arc = self.get_network_parameter(neo4JQuery.NUMBER_OF_I_ARC)
        self.number_of_c_arc = self.get_network_parameter(neo4JQuery.NUMBER_OF_C_ARC)
        self.number_of_communities = self.get_network_parameter(neo4JQuery.GET_NUMBER_OF_COMMUNITIES)
        self.nodes_for_community = self.get_nodes_for_community()
        self.objects_with_instances = self.read_objects_with_instances()
        self.list_instances = self.read_instances()
        self.resilience_system_nodes = self.get_resilience_system_nodes()

    def generate_transaction(self, code, start_instance, end_instance, context, file_format, size, failure_rate):
        return TrustedTransaction.TrustedTransaction(code, start_instance, end_instance,
                                                     context, file_format, size, failure_rate)

    def get_nodes_for_community(self):
        query_result = self.execute_query(neo4JQuery.GET_NODES_FOR_COMMUNITY)
        community = {}
        for x in query_result:
            community[x["community"]] = x["nodes"]
        return community



    def get_instances_linked_to(self, start_instance):
        query = neo4JQuery.GET_INSTANCES_LINKED_TO[0] + start_instance + neo4JQuery.GET_INSTANCES_LINKED_TO[1]
        result_query = self.execute_query(query)
        list_instances = []
        for result in result_query:
            list_instances.append(self.list_instances[result["linked"]["code"]])
        return list_instances

    def read_objects_with_instances(self):
        objects = {}
        result_query = self.execute_query(neo4JQuery.GET_OBJECTS_WITH_INSTANCES)
        for result in result_query:
            objects[result["obj"]] = result["instances"]
        return objects

    def read_instances(self):
        result_query = self.execute_query(neo4JQuery.GET_INSTANCES)
        list_instances = {}
        community_without_data_repository = [str(x) for x in range(1, self.number_of_communities + 1)]
        for instance in result_query:
            if instance["i"]["community"] in community_without_data_repository:
                list_instances[instance["i"]["code"]] = TrustedInstance.TrustedInstance(instance["i"], True)
                community_without_data_repository.remove(instance["i"]["community"])
            else:
                list_instances[instance["i"]["code"]] = TrustedInstance.TrustedInstance(instance["i"], False)
        return list_instances

    def get_network_parameter(self, query):
        result = self.execute_query(query)
        for x in result:
            return x[neo4JQuery.FIELD_PARAMETER]

    def set_parameter(self, query):
        self.execute_query(query)

    def object_in_the_same_network(self, ins1, ins2):
        result_query = self.execute_query(neo4JQuery.shortest_path(ins1, ins2))
        path = []
        community = set()
        for result in result_query:
            path = result["path"]
        for instance in path:
            community.add(instance["community"])
        # if transaction passes through different network and comes back initial network
        if len(community) == 1:
            return True
        else:
            return False

    def get_shortest_path_instances(self, ins1, ins2):
        result_query = self.execute_query(neo4JQuery.shortest_path(ins1, ins2))
        pairwise_instances = []
        path = []
        for result in result_query:
            path = result["path"]
        for i in range(0, len(path) - 1):
            pairwise_instances.append((path[i], path[i+1]))
        return pairwise_instances

    def get_community_from_instance(self, ins):
        return self.get_network_parameter(neo4JQuery.get_community_from_instance(ins))

    def get_instance_from_code(self, ins):
        return self.list_instances[ins]

    def check_behavioral_neighbors(self, ins1, ins2):
        return self.get_network_parameter(neo4JQuery.check_behavioral_neighbors(ins1, ins2))

    def get_number_of_communities(self):
        return self.get_network_parameter(neo4JQuery.GET_NUMBER_OF_COMMUNITIES)

    def get_instances_from_community(self, community):
        result_query = self.execute_query(neo4JQuery.get_instances_from_community(community))
        instances = []
        for result in result_query:
            instances.append(result["instances"])
        return instances

    def get_objects_from_community(self, community):
        return self.get_network_parameter(neo4JQuery.get_objects_from_community(community))

    def get_resilience_system_nodes(self):
        resilience_nodes = []
        if settings.COMPUTE_SYSTEM_RESILIENCE:
            num_resilience_nodes = int(self.number_of_instances * settings.PERCENTAGE_NODE_SYSTEM_RESILIENCE)
            i = 0
            while i < num_resilience_nodes:
                random_node = random.choice(self.list_instances.keys())
                if random_node not in resilience_nodes:
                    resilience_nodes.append(random_node)
                    i += 1
        return resilience_nodes
