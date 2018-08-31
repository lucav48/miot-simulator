from graph_dataset.create_dataset.tools import utilities, ReadFile
from shapely.geometry import LineString
from shapely.ops import nearest_points
from threading import Thread
from graph_dataset.create_dataset.neo4JHandler import Neo4JManager, Objects, Instance, Transaction
import settings
import random
import os
import re


# nodes is composed by 4 parts: descriptive, technical, travel path, code id
def create_objects():
    i = 0
    list_objects = []
    while i < settings.NUMBER_OF_NODES:
        des = random.choice(readFile.descriptive_array)
        # des[0] is id of that descriptive row
        tec = choose_technical_given_descriptive(des[0])
        code = str(i)
        new_node = Objects.Objects(des, tec, code, [])
        list_objects.append(new_node)
        i += 1
    return list_objects


def choose_technical_given_descriptive(tec_id):
    result = ""
    for tec in readFile.technical_array:
        if tec[-1] == tec_id:
            result = tec
    return result


def get_instances(list_objects):
    list_instances = []
    for one_object in list_objects:
        for i in one_object.instances:
            list_instances.append(i)
    return list_instances


def setup_and_create_connections(list_instances):
    threads = [None] * settings.NUMBER_OF_THREAD
    results_list = [None] * settings.NUMBER_OF_THREAD
    interval = int(len(list_instances) / settings.NUMBER_OF_THREAD)
    all_instances = get_instances(objects)
    for i in range(len(threads)):
        min_instance = interval * i
        max_instance = interval * (i+1)
        if (i+1) == len(threads):
            if interval * settings.NUMBER_OF_THREAD < len(list_instances):
                max_instance += len(list_instances) - (interval * settings.NUMBER_OF_THREAD)
        threads[i] = Thread(target=create_connections, args=(all_instances, min_instance, max_instance,
                                                             len(list_instances), results_list, i))
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    results = [item for sublist in results_list for item in sublist]
    return results


def create_connections(list_instances, min_v, max_v, n_instances, results, index):
    connections = []
    for i in range(min_v, max_v):
        instance = list_instances[i]
        instance_path = instance.travel_path
        for j in range(i+1, n_instances):
            other_instance_path = list_instances[j].travel_path
            connected = utilities.check_two_paths(instance_path, other_instance_path)
            if connected:
                connections.append(instance.code + "-" + list_instances[j].code)
    results[index] = connections


def get_all_context():
    list_context = dict()
    for x in os.listdir(settings.CONTEXT_FOLDER):
        list_context[x.split(settings.SUFFIX_CONTEXT_FILE)[0]] = []
    return list_context


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


def create_transactions(list_instances, con):
    i = 0
    transactions_list = []
    while i < settings.NUMBER_OF_TRANSACTIONS:
        # choose node where create a new transaction
        instance_start = random.choice(list_instances)
        # choose a node connected to node_start
        instance_connected = neoManager.neo4j_retrieve_connected_instances(instance_start.code)
        # check if node is isolated
        if instance_connected:
            instance_end = random.choice(instance_connected)
            sign = instance_start.code + "-" + instance_end
            # choose context
            new_context = choose_transaction_context(sign, con)
            # choose message from context
            message, timestamp = choose_message_from_context(new_context)
            # create transaction/8
            new_transaction = Transaction.Transaction(instance_start.code, instance_end, timestamp, new_context, message)
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


def create_instances_of_objects(object_list):
    for one_object in object_list:
        if isinstance(settings.NUMBER_OF_INSTANCES, (list,)):
            num_instance = random.choice(settings.NUMBER_OF_INSTANCES)
        else:
            num_instance = settings.NUMBER_OF_INSTANCES

        for i in range(0, num_instance):
            # travel has to be unique among nodes
            travel_index = random.choice(range(0, len(readFile.travel_array)))
            travel = readFile.travel_array[travel_index]
            del readFile.travel_array[travel_index]
            instance_code = one_object.code + ":" + str(i)
            one_object.instances.append(Instance.Instance(travel, instance_code))


def prepare_environment():
    # read metadata
    print "Read metadata."
    readFile.read_all()
    # read content files
    print "Read context file."
    all_context = get_all_context()
    readFile.read_all_context(all_context)
    print "Ready to start!"
    return all_context


def prepare_nodes():
    # create a list of object
    print "Objects creation.."
    list_objects = create_objects()
    # write neo4j queries to represent those nodes
    neoManager.neo4j_create_objects(list_objects)
    print "Objects created."
    # create instances of each object
    create_instances_of_objects(list_objects)
    all_instances = get_instances(list_objects)
    # create relationship between object and its instances
    neoManager.neo4j_create_objects_instances(list_objects)
    return list_objects, all_instances


def prepare_nodes_connections(list_objects):
    # look for connections among nodes
    print "Relationship creation.."
    connections = setup_and_create_connections(list_objects)
    # write neo4j queries to represent relationships
    neoManager.neo4j_create_connections(connections)
    print "Relationship created."


def prepare_transactions(list_instances, list_context):
    # now I have to create transactions
    print "Start transactions creation."
    transactions = create_transactions(list_instances, list_context)
    # write neo4j queries to represent those transactions
    neoManager.neo4j_add_transactions(transactions)
    print "Transactions creation completed."


def print_neo4j_queries():
    print "Started to write queries on db."
    utilities.write_to_file(neoManager)
    print "File ready to be loaded."


if __name__ == "__main__":
    # read data useful to create nodes
    print "Read and prepare to create dataset"
    readFile = ReadFile.ReadFile()
    neoManager = Neo4JManager.Neo4JManager()
    context = prepare_environment()
    objects, instances = prepare_nodes()
    prepare_nodes_connections(objects)
    prepare_transactions(instances, context)
    print_neo4j_queries()