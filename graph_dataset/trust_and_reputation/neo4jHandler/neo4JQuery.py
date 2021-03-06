from graph_dataset.trust_and_reputation import settings as settings
from graph_dataset.create_dataset import settings as create_settings
FIELD_PARAMETER = "parameter"

NUMBER_OF_INSTANCE = "MATCH(n:" + create_settings.NEO4J_INSTANCE_LABEL + ") RETURN COUNT(DISTINCT(n)) as " + \
                     FIELD_PARAMETER

NUMBER_OF_C_ARC = "MATCH(n:" + create_settings.NEO4J_INSTANCE_LABEL + ")-[r:" + \
                  create_settings.NEO4J_RELATION_INSTANCE_TYPE + "]-(n2:" + \
                  create_settings.NEO4J_INSTANCE_LABEL + \
                  ") WHERE n.community <> n2.community " \
                  "RETURN COUNT(DISTINCT(r)) as " + FIELD_PARAMETER

NUMBER_OF_I_ARC = "MATCH(n:" + create_settings.NEO4J_INSTANCE_LABEL + ")-[r:" +\
                  create_settings.NEO4J_RELATION_INSTANCE_TYPE + "]-(n2:" + \
                  create_settings.NEO4J_INSTANCE_LABEL + ") WHERE n.community = n2.community " \
                  "RETURN COUNT(DISTINCT(r)) as " + FIELD_PARAMETER

SET_INITIAL_TRUST = "MATCH(n:" + create_settings.NEO4J_INSTANCE_LABEL + ") SET n.trust = " + \
                    str(settings.INITIAL_TRUST_VALUE)

GET_INSTANCES = "MATCH(n:" + create_settings.NEO4J_INSTANCE_LABEL + ") RETURN DISTINCT(n) AS i"


GET_INSTANCES_LINKED_TO = ["MATCH(n:" + create_settings.NEO4J_INSTANCE_LABEL + ")" +
                           "-[:" + create_settings.NEO4J_RELATION_INSTANCE_TYPE + "*1]-" +
                           "(n2:" + create_settings.NEO4J_INSTANCE_LABEL + ") " +
                           "WHERE n.code = '",
                           "' RETURN DISTINCT(n2) AS linked"]

GET_NUMBER_OF_COMMUNITIES = "MATCH(n:Instance) RETURN COUNT(DISTINCT(n.community)) AS " + FIELD_PARAMETER

GET_OBJECTS = "MATCH(o:Object) RETURN COLLECT(o.code) AS " + FIELD_PARAMETER

GET_OBJECTS_WITH_INSTANCES = "MATCH(o:Object)-[:HAS_INSTANCE]-(n:Instance) RETURN o.code AS obj, " \
                             "COLLECT(n.code) AS instances"

GET_NODES_FOR_COMMUNITY = "MATCH(n:Instance) RETURN DISTINCT(n.community) AS community, count(n.community) AS nodes"


def check_behavioral_neighbors(ins1, ins2):
    return "MATCH(n1:Instance)-[:LINKED*1]-(n2:Instance) " \
           "WHERE n1.code='" + ins1 + "' AND n2.code = '" + ins2 + "' RETURN count(n1)=1 AS " + FIELD_PARAMETER


def shortest_path(ins1, ins2):
    return "MATCH(n1:Instance),(n2:Instance),p=shortestPath((n1)-[:LINKED*1..3]-(n2)) " \
           "WHERE n1.code='" + ins1 + "' AND n2.code='" + ins2 + "' RETURN nodes(p) AS path"


def get_community_from_instance(ins):
    return "MATCH(n:Instance) WHERE n.code='" + ins + "' RETURN n.community AS " + FIELD_PARAMETER


def get_instance_from_code(ins):
    return "MATCH(n:Instance) WHERE n.code='" + ins + "' RETURN n AS " + FIELD_PARAMETER


def get_instances_from_community(community):
    return "MATCH(n:Instance) WHERE n.community ='" + str(community) + "' "\
           "RETURN distinct(n.code) AS instances"


def get_objects_from_community(community):
    return "MATCH(o:Object)-[:HAS_INSTANCE]->(n:Instance) " \
           "WHERE n.community = '" + community + "' " \
            "RETURN COLLECT(o.code) AS " + FIELD_PARAMETER
