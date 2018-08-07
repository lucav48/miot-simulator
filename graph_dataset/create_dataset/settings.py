NUMBER_OF_NODES = 100
METADATA_FOLDER = "metadata"
DESCRIPTIVE_CSV = METADATA_FOLDER + "/" + "descriptive_metadata.csv"
TECHNICAL_CSV = METADATA_FOLDER + "/" + "technical_metadata.csv"
BEHAVIORAL_CSV = METADATA_FOLDER + "/" + "Posts.xml"
TRAVEL_CSV = METADATA_FOLDER + "/" + "travel_metadata.csv"
LIMIT_METER_CONNECTION = 8

# neo4j settings
NEO4J_URI = "bolt://localhost"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "python"

NEO4J_DELETE_NODES = "MATCH (n) DETACH DELETE n"
NEO4J_RELATION_TYPE = "LINKED"
