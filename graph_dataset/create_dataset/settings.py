# settings of dataset to create
LIMIT_METER_CONNECTION = 150
NUMBER_OF_TRANSACTIONS = 10000
PROBABILITY_TO_CHOOSE_FROM_CONTEXT_ALREADY_USED = 0.7
NUMBER_OF_CONTENT_MESSAGES_TO_READ = 10
# it could be random between [min,max] or a number
# put instances you want in right place of list!
# Example: [4, 5, 6] will create for 4 object with 1 instance, 5 object with 2 instances and 6 objects with 3 instances
NUMBER_OF_INSTANCES = [125, 22, 9]
NUMBER_OF_OBJECTS = sum(NUMBER_OF_INSTANCES)
NUMBER_OF_COMMUNITIES = 11
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
BEHAVIORAL_CSV = METADATA_FOLDER + "/" + "Posts.xml"
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
