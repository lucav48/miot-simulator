from graph_dataset.create_dataset import settings
import time


def write_to_file(neoManager):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_file = open(settings.PREFIX_DATASET_FILE + timestr + settings.CREATED_DATASET_EXTENSION, "w")

    # add objects
    output_file.write(":begin\n")
    print_list(output_file, neoManager.neo4j_create_nodes_query)
    output_file.write("\n:commit\n")
    # add objects
    output_file.write(":begin\n")
    print_list(output_file, neoManager.neo4j_create_instances_query)
    output_file.write("\n:commit\n")
    # add relationships
    output_file.write(":begin\n")
    print_list(output_file, neoManager.neo4j_create_connections_query)
    output_file.write("\n:commit\n")
    # add transactions
    output_file.write(":begin\n")
    print_list(output_file, neoManager.neo4j_create_transactions_query)
    output_file.write("\n:commit\n")
    # adjust communities transactions
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_adjust_communities_query)
    output_file.write("\n:commit\n")
    # adjust communities transactions
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_delete_isolated_nodes_query)
    output_file.write("\n:commit\n")
    output_file.close()


def print_list(output_file, list_to_print):
    limit_rows = 100000
    if len(list_to_print) > limit_rows:
        times = len(list_to_print) / limit_rows
        for i in range(0, times):
            list_to_print.insert(limit_rows * (i+1), ":commit\n :begin")
    for element in list_to_print:
        output_file.write("\n" + element.encode('utf-8') + ";")
