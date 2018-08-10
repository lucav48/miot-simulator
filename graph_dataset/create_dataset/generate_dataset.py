import ReadFile
import Neo4JManager
import settings
import random
import ast
import utilities
import os
import Node
import Transaction
import write_dataset_to_file
import re
from threading import Thread
import math
import numpy as np

# nodes is composed by 4 parts: descriptive, technical, travel path, code id
def create_nodes(readFile):
    i = 0
    list_nodes = []
    travel_already_chosen = []
    while i < settings.NUMBER_OF_NODES:
        des = random.choice(readFile.descriptive_array)
        tec = random.choice(readFile.technical_array)
        # travel has to be unique among nodes
        travel = random.choice(readFile.travel_array)
        while travel in travel_already_chosen:
            travel = random.choice(readFile.travel_array)
        code = str(i)
        new_node = Node.Node(des, tec, travel, code, "")
        list_nodes.append(new_node)
        i += 1
    return list_nodes


def setup_and_create_connections(nodes_list):
    threads = [None] * settings.NUMBER_OF_THREAD
    results_list = [None] * settings.NUMBER_OF_THREAD
    interval = int(len(nodes_list) / settings.NUMBER_OF_THREAD)
    for i in range(len(threads)):
        min_node = interval * i
        max_node = interval * (i+1)
        if (i+1) == len(threads):
            if interval * settings.NUMBER_OF_THREAD < len(nodes_list):
                max_node += len(nodes_list) - (interval * settings.NUMBER_OF_THREAD)
        threads[i] = Thread(target=create_connections, args=(nodes_list[min_node:max_node], results_list, i))
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    results = [item for sublist in results_list for item in sublist]
    return results


def create_connections(list_nodes, results, index):
    connections = []
    n_nodes = len(list_nodes)
    for i in range(n_nodes):
        node = list_nodes[i]
        node_path = utilities.literal_eval(node.travel_path)
        for j in range(i+1, n_nodes):
            other_node_path = utilities.literal_eval(list_nodes[j].travel_path)
            connected = utilities.check_two_paths(node_path, other_node_path)
            if connected:
                connections.append(node.code + "-" + list_nodes[j].code)
    results[index] = connections
    print connections


def get_all_context():
    context = dict()
    for x in os.listdir(settings.CONTEXT_FOLDER):
        context[x.split(settings.SUFFIX_CONTEXT_FILE)[0]] = []
    return context


def choose_transaction_context(sign, all_context):
    # look for context already used by those nodes
    talked_about = []
    for key, value in all_context.items():
        if sign in value:
            talked_about.append(key)

    # if this is first transaction
    if not talked_about:
        content_result = random.choice(all_context.keys())
        all_context[content_result] = sign
    # if this isn't first transaction
    else:
        probability = random.randint(0, 1)
        if probability < settings.PROBABILITY_TO_CHOOSE_FROM_CONTEXT_ALREADY_USED:
            content_result = random.choice(talked_about)
        else:
            content_result = random.choice(all_context.keys())
            all_context[content_result] = sign
    return content_result


def create_transactions(nodes, con):
    i = 0
    transactions_list = []
    while i < settings.NUMBER_OF_TRANSACTIONS:
        # choose node where create a new transaction
        node_start = random.choice(nodes)
        node_end = random.choice(nodes)
        while node_start == node_end:
            node_end = random.choice(nodes)
        # check if nodes are connected by a path in graph
        result = neoManager.check_if_nodes_connected(node_start.code, node_end.code)
        sign = node_start.code + "-" + node_end.code
        if result == sign:
            # choose context
            context = choose_transaction_context(sign, con)
            # choose message from context
            message, timestamp = choose_message_from_context(context)
            # create transaction
            new_transaction = Transaction.Transaction(node_start.code, node_end.code, timestamp, context, message)
            transactions_list.append(new_transaction)
            i += 1
    return transactions_list


def choose_message_from_context(con):
    row = random.choice(readFile.context_dict[con])
    message = row.attributes["Body"].value
    timestamp = row.attributes["CreationDate"].value
    message = re.sub("[\"!@#$%^&*()[]{};:,./<>?\|`~-=_+]", " ", message)
    message = message.replace("\n", "")
    message = message.replace("'", "")
    message = message.replace(",", "")
    return message, timestamp


if __name__ == "__main__":
    # read data useful to create nodes
    print "Read and prepare to create dataset"
    readFile = ReadFile.ReadFile()
    neoManager = Neo4JManager.Neo4JManager()
    # read metadata
    print "Read metadata."
    readFile.read_all()
    # read content files
    print "Read context file."
    context = get_all_context()
    readFile.read_all_context(context)
    print "Ready to start!"
    # create a list of nodes
    print "Node creation.."
    nodes = create_nodes(readFile)
    # write neo4j queries to represent those nodes
    neoManager.neo4j_create_nodes(nodes)
    print "Nodes created."
    # look for connections among nodes
    print "Relationship creation.."
    connections = setup_and_create_connections(nodes)
    # write neo4j queries to represent relationships
    neoManager.neo4j_create_connections(connections)
    print "Relationship created."
    # # now I have to create transactions
    # print "Start transactions creation."
    # transactions = create_transactions(nodes, context)
    # # write neo4j queries to represent those transactions
    # neoManager.neo4j_add_transactions(transactions)
    # print "Transactions creation completed."
    # # write_dataset_to_file.write_to_file(neoManager)
