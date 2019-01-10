# settings of dataset to create
LIMIT_METER_CONNECTION = 100
NUMBER_OF_TRANSACTIONS = 0
PROBABILITY_TO_CHOOSE_FROM_CONTEXT_ALREADY_USED = 0.7
NUMBER_OF_CONTENT_MESSAGES_TO_READ = 10
# put instances you want in right place of list!
# Example: [4, 5, 6] will create for 4 object with 1 instance, 5 object with 2 instances and 6 objects with 3 instances
NUMBER_OF_INSTANCES = [60, 0, 0]
NUMBER_OF_OBJECTS = sum(NUMBER_OF_INSTANCES)
# COMMUNITY_LEADERS = [(41.17853, -8.66743), (41.15325, -8.676), (41.13944, -8.63739), (41.14151, -8.61452),
#                     (41.1435, -8.58582), (41.16323, -8.58395), (41.17865, -8.58418), (41.18464, -8.60747),
#                     (41.1841, -8.6417), (41.15352, -8.60554)]
NUMBER_OF_COMMUNITIES = 1
PERCENTAGE_C_ARC = 0.2
ADJUST_COMMUNITIES = 1
DELETE_ISOLATED_NODES = 1
CLEAR_ALL_NEO4J = 0
# execution settings
NUMBER_OF_THREAD = 1

# folder structure
METADATA_FOLDER = "metadata"
CREATED_DATASET_FOLDER = "dataset"
DESCRIPTIVE_CSV = METADATA_FOLDER + "/" + "descriptive_metadata.csv"
TECHNICAL_CSV = METADATA_FOLDER + "/" + "technical_metadata.csv"
TRAVEL_CSV = METADATA_FOLDER + "/" + "travel_metadata.csv"
TRAVEL_JSON = METADATA_FOLDER + "/" + "travel_distances.txt"
CONTEXT_FOLDER = METADATA_FOLDER + "/" + "context"
SUFFIX_CONTEXT_FILE = "Posts.xml"
PREFIX_DATASET_FILE = CREATED_DATASET_FOLDER + "/" + "network-"
CREATED_DATASET_EXTENSION = ".cyp"

# neo4j label and relationship name
NEO4J_DELETE_NODES = "MATCH (n) DETACH DELETE n"
NEO4J_RELATION_INSTANCE_TYPE = "LINKED"
NEO4J_RELATION_TRANSACTION_TYPE = "HAS_TRANSACTION"
NEO4J_RELATION_OBJECT_INSTANCE_TYPE = "HAS_INSTANCE"
NEO4J_OBJECT_LABEL = "Object"
NEO4J_INSTANCE_LABEL = "Instance"
NEO4J_TRANSACTION_LABEL = "Transaction"
