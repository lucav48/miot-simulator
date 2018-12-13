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
                           "-[:" + create_settings.NEO4J_RELATION_INSTANCE_TYPE + "*1..3]-" +
                           "(n2:" + create_settings.NEO4J_INSTANCE_LABEL + ") " +
                           "WHERE n.code = '",
                           "' RETURN DISTINCT(n2) AS linked"]

GET_NUMBER_OF_COMMUNITIES = "MATCH(n:Instance) RETURN COUNT(DISTINCT(n.community)) AS " + FIELD_PARAMETER
