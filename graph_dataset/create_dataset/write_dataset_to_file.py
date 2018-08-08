import settings
import time


def write_to_file(neoManager):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_file = open(settings.PREFIX_DATASET_FILE + timestr + settings.CREATED_DATASET_EXTENSION, "w")

    for row in neoManager.neo4j_create_nodes_query:
        output_file.write(row)

    for row in neoManager.neo4j_create_connections_query:
        output_file.write(row)

    output_file.close()
