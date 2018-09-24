from graph_dataset.create_dataset.neo4JHandler.Neo4JInstance import Neo4JInstance
from graph_dataset.create_dataset.neo4JHandler.neo4JObject import Transaction
from graph_dataset.create_dataset.neo4JHandler.neo4JObject import Instance
from graph_dataset.create_dataset.neo4JHandler.neo4JObject import Object


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
        query = "MATCH(n:Instance)-[r:LINKED]->(n2:Instance) RETURN COUNT(r) as relationships"
        query_result = self.execute_query(query)
        n_relationships = 0
        for row in query_result:
            n_relationships = row["relationships"]
        # average number of neighborhood
        query = "MATCH(n:Instance)-[r:LINKED]->(n2:Instance) WITH n, count(n2) as nodes return avg(nodes) as average"
        query_result = self.execute_query(query)
        avg_neighborhood = 0
        for row in query_result:
            avg_neighborhood = round(row["average"], 2)
        return n_nodes, n_transactions, n_relationships, avg_neighborhood