from graph_dataset.create_dataset.neo4JHandler.Neo4JInstance import Neo4JInstance
from graph_dataset.create_dataset.neo4JHandler.neo4JObject import Transaction
from graph_dataset.create_dataset.neo4JHandler.neo4JObject import Instance
from graph_dataset.create_dataset.neo4JHandler.neo4JObject import Object
from graph_dataset.create_dataset import settings as create_settings
import random


class Neo4JManager(Neo4JInstance):
    def __init__(self):
        # get neo4j instance
        Neo4JInstance.__init__(self)

    def get_transactions(self):
        query = "MATCH(n:Instance)-[:HAS_TRANSACTION]->(t:Transaction)-[:HAS_TRANSACTION]->(n2:Instance)" \
                + "RETURN n.code as node1, collect(t) as transactions, n2.code as node2 ORDER BY node1"
        query_result = self.execute_query(query)
        transactions = {}
        for x in query_result:
            key_transaction = x["node1"] + "-" + x["node2"]
            transactions[key_transaction] = []
            for t in x["transactions"]:
                transactions[key_transaction].append(Transaction.Transaction(t["code"],
                                                                             x["node1"],
                                                                             x["node2"],
                                                                             "",
                                                                             t["context"],
                                                                             ""))
        return transactions

    def get_all_instances(self):
        query = "MATCH(n:Instance) RETURN n.code as code, n.community as community ORDER BY code"
        query_result = self.execute_query(query)
        instances = []
        for node in query_result:
            instances.append(Instance.Instance(
                path="",
                code=node["code"],
                num_community=node["community"]
            ))
        return instances

    def get_all_objects(self):
        query = "MATCH(n:Object)-[:HAS_INSTANCE]-(i:Instance) RETURN n.code as code, collect(i.code) as instances " \
                "ORDER BY code "
        query_result = self.execute_query(query)
        objects = []
        for node in query_result:
            instances = []
            for instance in node["instances"]:
                instances.append(Instance.Instance(path="", code=instance, num_community=""))
            objects.append(Object.Object(
                des="",
                tec="",
                code=node["code"],
                instances=instances,
                n_instances=len(node["instances"])))
        return objects

    def get_neighborhoods(self):
        query = "MATCH(n:Instance)-[:HAS_TRANSACTION]-(:Transaction)-[:HAS_TRANSACTION]-(n2:Instance) " \
                "RETURN n.code as code, collect(n2.code) as instances"
        query_result = self.execute_query(query)
        instances = {}
        for node in query_result:
            local_neighborhood = []
            for i in node["instances"]:
                local_neighborhood.append(Instance.Instance(path="", code=i, num_community=""))
            instances[node["code"]] = local_neighborhood
        return instances

    def check_community_connected_nodes(self, node1, node2):
        query = "MATCH(n1:Instance)-[r:LINKED]-(n2:Instance)" \
                "WHERE n1.code='" + node1 + "' AND n2.code='" + node2 + "' " \
                "RETURN r as relation, n1.community as community1, n2.community as community2"
        query_result = self.execute_query(query)
        comm1 = -1
        comm2 = -1
        for result in query_result:
            comm1 = result["community1"]
            comm2 = result["community2"]
        return comm1, comm2

    def get_communities_neighborhood(self, code):
        query = "MATCH(n:Instance)-[:LINKED]-(n2:Instance) "\
                "WHERE n.code='" + code + "' " \
                "RETURN n2.code as code, " \
                    "CASE WHEN n.community = n2.community THEN True ELSE False END as result"
        query_result = self.execute_query(query)
        results = {}
        for res in query_result:
            results[res["code"]] = res["result"]
        return results

    def get_instances_to_merge_unsupervised(self):
        query = "MATCH(o:Object)-[:HAS_INSTANCE]->(n:Instance), "\
                "(o)-[:HAS_INSTANCE]->(n2:Instance) " \
                "WHERE n.community<> n2.community "\
                "RETURN n.code as node, collect(n2.code) as connected"
        query_result = self.execute_query(query)
        instances_list = {}
        for row in query_result:
            index = row["node"]
            instances_list[index] = []
            for n in row["connected"]:
                instances_list[index].append(n)

        return instances_list

    def get_instances_connections(self):
        query = "MATCH(n:Instance)-[r:LINKED]-(n2:Instance) " \
                "RETURN n.code as node, collect(n2.code) as connections"
        query_result = self.execute_query(query)
        connections = {}
        for row in query_result:
            connections[row["node"]] = row["connections"]
        return connections

    def get_network_values(self):
        # number of nodes
        query = "MATCH(n:Instance) RETURN COUNT(n) as nodes"
        query_result = self.execute_query(query)
        n_nodes = 0
        for row in query_result:
            n_nodes = row["nodes"]
        # number of transactions
        query = "MATCH(t:Transaction) RETURN COUNT(t) as transactions"
        query_result = self.execute_query(query)
        n_transactions = 0
        for row in query_result:
            n_transactions = row["transactions"]
        # number of relationships
        query = "MATCH(n:Instance)-[r:LINKED]-(n2:Instance) RETURN COUNT(DISTINCT(r)) as relationships"
        query_result = self.execute_query(query)
        n_relationships = 0
        for row in query_result:
            n_relationships = row["relationships"]
        # number of c arch
        query = "MATCH(n:Instance)-[r:LINKED]-(n2:Instance) WHERE n.community <> n2.community " \
                "RETURN COUNT(DISTINCT(r)) as relationships"
        query_result = self.execute_query(query)
        n_carch = 0
        for row in query_result:
            n_carch = row["relationships"]
        # number of i arch
        query = "MATCH(n:Instance)-[r:LINKED]-(n2:Instance) WHERE n.community = n2.community " \
                "RETURN COUNT(DISTINCT(r)) as relationships"
        query_result = self.execute_query(query)
        n_iarch = 0
        for row in query_result:
            n_iarch = row["relationships"]
        # average number of neighborhood
        query = "MATCH(n:Instance)-[r:LINKED]->(n2:Instance) WITH n, count(n2) as nodes return avg(nodes) as average"
        query_result = self.execute_query(query)
        avg_neighborhood = 0
        for row in query_result:
            avg_neighborhood = round(row["average"], 2)
        triangle_count, avg_cluster_coefficient = self.get_clustering_coefficient()
        list_cluster_coefficients = self.get_cluster_cofficients_of_each_community()
        list_density_communities = self.get_density_communities()
        # get number of instances according to objects
        query = "MATCH(o:Object)-[:HAS_INSTANCE]->(n:Instance) " +\
                "WITH o.code as obj, collect(n.code) AS instances " +\
                "RETURN count(obj) as num_objects, size(instances) as num_instances"
        query_result = self.execute_query(query)
        message_list_obj_instances = "Instances per object: "
        for row in query_result:
            message_list_obj_instances = message_list_obj_instances + str(row["num_objects"]) + " objects has " +\
                str(row["num_instances"]) + " instances. "
        return n_nodes, n_transactions, n_relationships, n_iarch, n_carch, avg_neighborhood, triangle_count, \
            avg_cluster_coefficient, list_cluster_coefficients, list_density_communities, message_list_obj_instances

    def get_density_communities(self):
        community_list = list(range(1, create_settings.NUMBER_OF_COMMUNITIES + 1))
        result_as_string = ""
        for community in community_list:
            result_as_string += str(community) + ": "
            query = "MATCH(n1:Instance)-[r:LINKED]-(n2:Instance) " \
                    "WHERE n1.community = '" + str(community) + "' AND n2.community = '" + str(community) + "' " \
                    "RETURN count(distinct(n1)) as nodes, count(r) as relationships"
            query_result = self.execute_query(query)
            for result in query_result:
                nodes = result["nodes"]
                relationships = result["relationships"]
                density = (2.0 * relationships) / (nodes * (nodes - 1))
                result_as_string += str(round(density, 3)) + "  "
        return result_as_string

    def get_cluster_cofficients_of_each_community(self):
        community_list = list(range(1, create_settings.NUMBER_OF_COMMUNITIES + 1))
        result_as_string = ""
        for community in community_list:
            result_as_string += str(community) + ": "
            query = "CALL algo.triangleCount('MATCH(n:Instance) WHERE n.community=\"" + str(community) + "\" " +\
                    " RETURN id(n) as id','MATCH(n1:Instance)-[:LINKED]-(n2:Instance) WHERE n1.community=\"" + str(community) + "\" "\
                    " AND n2.community=\"" + str(community) + "\" " +\
                    " RETURN id(n1) as source, id(n2) as target',{concurrency:4, graph:'cypher'," \
                    " clusteringCoefficientProperty:'coefficient'})" \
                    " YIELD nodeCount, triangleCount, averageClusteringCoefficient"
            self.execute_query(query)
            query = "MATCH(n:Instance) WHERE n.community='" + str(community) + "' RETURN n.coefficient as coefficient"
            query_result = self.execute_query(query)
            avg_clustering = 0
            n_nodes = 1
            for result in query_result:
                cluster_coeff = result["coefficient"]
                if cluster_coeff != float('inf'):
                    avg_clustering += float(cluster_coeff)
                    n_nodes += 1
            avg_clustering = round(avg_clustering / n_nodes, 3)
            result_as_string += str(avg_clustering) + "  "
        return result_as_string

    def get_clustering_coefficient(self):
        query = "CALL algo.triangleCount('Instance','LINKED', "\
                "{concurrency:4}) "\
                "YIELD triangleCount, averageClusteringCoefficient"
        query_result = self.execute_query(query)
        triangle_count = 0
        avg_cluster_coefficient = 0
        for result in query_result:
            triangle_count = result["triangleCount"]
            avg_cluster_coefficient = result["averageClusteringCoefficient"]
        return triangle_count, avg_cluster_coefficient

    def get_node_by_bfs_at_distance(self, start_node, neo4j_list_nodes, distance):
        nodes_level = []
        end_node_found = False
        end_node = -1
        count_nodes = 0
        nodes_visited = []
        for i in range(1, distance + 1):
            query = "MATCH(n:Instance)-[:LINKED*" + str(i) + ".." + str(i) + "]-(n2:Instance) " \
                    "WHERE n.code='" + start_node + "' " \
                    "RETURN n.code as code, collect(DISTINCT(n2.code)) as connected_nodes"
            query_result = self.execute_query(query)
            for result in query_result:
                nodes_this_level = self.difference_list(result["connected_nodes"], nodes_visited)
                nodes_level.append(nodes_this_level)
                if i != distance:
                    count_nodes += len(nodes_this_level)
                    nodes_visited = nodes_visited + nodes_this_level
                else:
                    half_length = len(nodes_this_level) / 2
                    count_nodes += half_length
                    nodes_visited = nodes_visited + nodes_this_level[:half_length]
        if len(nodes_level) >= (distance - 1):
            choose_from = nodes_level[distance - 1]
            while not end_node_found:
                end_node = random.choice(choose_from)
                choose_from.remove(end_node)
                if end_node in neo4j_list_nodes:
                    end_node_found = True
                elif len(choose_from) == 0:
                    end_node_found = True
        return nodes_visited, count_nodes, end_node

    def difference_list(self, l1, l2):
        return list(set(l1) - set(l2))

    def get_distribution_nodes_on_communities(self):
        community_nodes = {}
        for i in range(1, create_settings.NUMBER_OF_COMMUNITIES + 1):
            query = "MATCH (n:Instance) WHERE n.community='" + str(i) + "' RETURN count(n) AS cont"
            query_result = self.execute_query(query)
            for result in query_result:
                community_nodes[str(i)] = result["cont"]
        return community_nodes
