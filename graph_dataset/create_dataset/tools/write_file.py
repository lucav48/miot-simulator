from graph_dataset.create_dataset import settings
import time


def write_to_file(neoManager):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_file = open(settings.PREFIX_DATASET_FILE + timestr + settings.CREATED_DATASET_EXTENSION, "w")

    # add objects
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_nodes_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # add objects
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_instances_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # add relationships
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_connections_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # add transactions
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_transactions_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # adjust communities transactions
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_adjust_communities_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # adjust communities transactions
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_delete_isolated_nodes_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    output_file.close()
