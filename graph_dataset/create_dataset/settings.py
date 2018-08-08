# settings of dataset to create
NUMBER_OF_NODES = 10
LIMIT_METER_CONNECTION = 4

# folder structure
METADATA_FOLDER = "metadata"
CREATED_DATASET_FOLDER = "created_dataset"
DESCRIPTIVE_CSV = METADATA_FOLDER + "/" + "descriptive_metadata.csv"
TECHNICAL_CSV = METADATA_FOLDER + "/" + "technical_metadata.csv"
BEHAVIORAL_CSV = METADATA_FOLDER + "/" + "Posts.xml"
TRAVEL_CSV = METADATA_FOLDER + "/" + "travel_metadata.csv"
CONTEXT_FOLDER = METADATA_FOLDER + "/" + "context"
SUFFIX_CONTEXT_FILE = "Posts"
PREFIX_DATASET_FILE = CREATED_DATASET_FOLDER + "/" + "network-"
CREATED_DATASET_EXTENSION = ".txt"

# neo4j settings
NEO4J_URI = "bolt://localhost"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "python"

NEO4J_DELETE_NODES = "MATCH (n) DETACH DELETE n"
NEO4J_RELATION_TYPE = "LINKED"
