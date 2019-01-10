from graph_dataset.create_dataset.tools import utilities, ReadFile, write_file
from graph_dataset.create_dataset.neo4JHandler import Neo4JManager
from graph_dataset.create_dataset.neo4JHandler.neo4JObject import Object, Instance, Transaction
from threading import Thread
import settings
import random
import os
import re


# nodes is composed by 4 parts: descriptive, technical, travel path, code id
def create_objects():
    i = 0
    list_objects = []
    list_instances = settings.NUMBER_OF_INSTANCES
    while i < settings.NUMBER_OF_OBJECTS:
        des = random.choice(readFile.descriptive_array)
        # des[0] is id of that descriptive row
        tec = choose_technical_given_descriptive(des[0])
        code = str(i)
        num_instances, list_instances = get_num_instances(list_instances)
        new_node = Object.Object(des, tec, code, [], num_instances)
        list_objects.append(new_node)
        i += 1
    return list_objects


def get_num_instances(num_instances):
    availables = [i for i, e in enumerate(num_instances) if e != 0]
    pos = random.choice(availables)
    num_instances[pos] -= 1
    return pos + 1, num_instances


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


def setup_and_create_connections(list_object, travel_distances):
    threads = [None] * settings.NUMBER_OF_THREAD
    results_query_list = [None] * settings.NUMBER_OF_THREAD
    results_connections_list = [None] * settings.NUMBER_OF_THREAD
    all_instances = get_instances(list_object)
    interval = int(len(all_instances) / settings.NUMBER_OF_THREAD)
    for i in range(len(threads)):
        min_instance = interval * i
        max_instance = interval * (i+1)
        if (i+1) == len(threads):
            if interval * settings.NUMBER_OF_THREAD < len(all_instances):
                max_instance += len(all_instances) - (interval * settings.NUMBER_OF_THREAD)
        threads[i] = Thread(target=create_connections, args=(all_instances, min_instance, max_instance,
                                                             len(all_instances), travel_distances,
                                                             results_query_list, results_connections_list, i))
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    # results_query = [item for sublist in results_query_list for item in sublist]
    results_connections = [item for sublist in results_connections_list for item in sublist]
    shaped_connections = shape_number_c_arc(results_connections)
    neoManager.create_connections_query(shaped_connections)
    return results_connections


def create_connections(list_instances, min_v, max_v, n_instances, travel_distances,
                       results_query, results_connections, index):
    connections_query = []
    connections_tuples = []
    for i in range(min_v, max_v):
        instance = list_instances[i]
        for j in range(i+1, n_instances):
            code1 = instance.code
            code2 = list_instances[j].code
            travel_code1 = instance.travel_path
            travel_code2 = list_instances[j].travel_path
            if int(travel_code1) < int(travel_code2):
                if travel_distances[travel_code1][travel_code2] < settings.LIMIT_METER_CONNECTION:
                    connection_type = "i"
                    if instance.community != list_instances[j].community:
                        connection_type = "c"
                    # connections_query.append(neoManager.create_query_connection(code1, code2))
                    connections_tuples.append((code1, code2, connection_type))
            else:
                if travel_distances[travel_code2][travel_code1] < settings.LIMIT_METER_CONNECTION:
                    connection_type = "i"
                    if instance.community != list_instances[j].community:
                        connection_type = "c"
                    # connections_query.append(neoManager.create_query_connection(code1, code2))
                    connections_tuples.append((code1, code2, connection_type))
            # connected = utilities.check_two_paths(instance.travel_path, list_instances[j].travel_path)
            # if connected:
            #     connections.append(instance.code + "-" + list_instances[j].code)
    # results_query[index] = connections_query
    results_connections[index] = connections_tuples
    print "Thread ", index, " finished to work."


def get_all_context():
    list_context = dict()
    for x in os.listdir(settings.CONTEXT_FOLDER):
        if os.path.isfile(x):
            list_context[x.split(settings.SUFFIX_CONTEXT_FILE)[0]] = []
    return list_context


def choose_transaction_context(instance_start, instance_end, all_context):
    # look for context already used by those nodes
    talked_about = []
    sign = instance_start + "-" + instance_end
    reverse_sign = instance_end + "-" + instance_start
    for key, value in all_context.items():
        if sign in value or reverse_sign in value:
            talked_about.append(key)
    # get context that instance start and end talked about
    talked_about_instance_start = []
    talked_about_instance_end = []
    for key, list_couple_instances in all_context.items():
        if list_couple_instances:
            for couple_instance in list_couple_instances:
                if instance_start == couple_instance.split("-")[0] or instance_start == couple_instance.split("-")[1]:
                    talked_about_instance_start.append(key)
                elif instance_end == couple_instance.split("-")[0] or instance_end == couple_instance.split("-")[1]:
                    talked_about_instance_end.append(key)
    intersect_talked_about = [x for x in talked_about_instance_start if x in talked_about_instance_end]
    # if this is first transaction
    if not talked_about:
        if intersect_talked_about:
            content_result = random.choice(intersect_talked_about)
        else:
            content_result = random.choice(all_context.keys())
        all_context[content_result].append(sign)
    # if this isn't first transaction
    else:
        probability = random.random()
        if probability < settings.PROBABILITY_TO_CHOOSE_FROM_CONTEXT_ALREADY_USED:
            content_result = random.choice(talked_about)
        else:
            if intersect_talked_about:
                content_result = random.choice(intersect_talked_about)
            else:
                content_result = random.choice(all_context.keys())
            all_context[content_result].append(sign)
    return content_result


def create_transactions(list_instances, list_connections, context_list):
    i = 0
    transactions_list = []
    while i < settings.NUMBER_OF_TRANSACTIONS:
        # choose node where create a new transaction
        instance_start = random.choice(list_instances).code
        # choose a node connected to node_start
        instance_connected = get_instance_connected(instance_start, list_connections)
        # check if node is isolated
        if instance_connected:
            # choose context
            new_context = choose_transaction_context(instance_start, instance_connected, context_list)
            # choose message from context
            message, timestamp = choose_message_from_context(new_context)
            # create transaction
            new_transaction = Transaction.Transaction(i, instance_start,
                                                      instance_connected, timestamp, new_context, message)
            transactions_list.append(new_transaction)
            i += 1
    return transactions_list


def get_instance_connected(instance_start, connections_list):
    instances_connected = [(x, y) for (x, y, _) in connections_list if x == instance_start or y == instance_start]
    if instances_connected:
        (x, y) = random.choice(instances_connected)
        if x == instance_start:
            return y
        else:
            return x
    else:
        return None


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
    travel_index_chosen = range(1, len(readFile.travel_array) - 1)
    num_instances = 0
    for one_object in object_list:
        community_chosen = []
        for i in range(0, one_object.num_instances):
            # travel has to be unique among nodes
            travel_index = random.choice(travel_index_chosen)
            # travel = utilities.travel_to_dataframe(readFile.travel_array[travel_index])
            travel_index_chosen.remove(travel_index)
            instance_code = one_object.code + ":" + str(i)
            # num_community = get_closest_community(str(travel_index), readFile)
            num_community = random.choice(range(1, settings.NUMBER_OF_COMMUNITIES + 1))
            while num_community in community_chosen:
                num_community = random.choice(range(1, settings.NUMBER_OF_COMMUNITIES + 1))
            community_chosen.append(num_community)
            one_object.instances.append(Instance.Instance(travel_index, instance_code, num_community))
            num_instances += 1
    print "Instances of objects created: ", str(num_instances)


def get_closest_community(travel_index, readFile):
    community = 0
    min_distance = 100000
    travel_string = readFile.travel_array[int(travel_index) - 1]
    travel_path = utilities.string_to_path(travel_string)
    for leader in settings.NUMBER_OF_COMMUNITIES:
        distance = utilities.calculate_haversine(travel_path, leader)
        if distance < min_distance:
            min_distance = distance
            community = settings.NUMBER_OF_COMMUNITIES.index(leader) + 1
    return community


def shape_number_c_arc(connections_list):
    # count number i arc
    n_iarc = []
    n_carc = []
    for (x, y, conn_type) in connections_list:
        if conn_type == "i":
            n_iarc.append((x, y, conn_type))
        else:
            n_carc.append((x, y, conn_type))
    print "Number of i-arc: ", str(len(n_iarc))
    print "Number of c-arc: ", str(len(n_carc))
    number_edges_to_delete = int(len(n_carc) - len(n_iarc) * settings.PERCENTAGE_C_ARC)
    number_c_arc = int(len(n_iarc) * settings.PERCENTAGE_C_ARC)
    print "C-arc deleted: ", str(number_edges_to_delete)
    final_connections_list = n_iarc
    carc_to_add = []
    if n_carc:
        i = 0
        while i < number_c_arc:
            new_edge = random.choice(n_carc)
            if new_edge not in carc_to_add:
                carc_to_add.append(new_edge)
                final_connections_list.append(new_edge)
                i += 1
    return final_connections_list


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
    print "Objects created: ", len(list_objects)
    # create instances of each object
    create_instances_of_objects(list_objects)
    all_instances = get_instances(list_objects)
    # create relationship between object and its instances
    neoManager.neo4j_create_objects_instances(list_objects)
    return list_objects, all_instances


def prepare_nodes_connections(list_objects, travel_distances):
    # look for connections among nodes
    print "Relationship creation.."
    connections_list = setup_and_create_connections(list_objects, travel_distances)
    print "Number of connections before shaping number of c-arc: ", len(connections_list)
    print "Relationship created."
    return connections_list


def prepare_transactions(list_instances, connections, list_context):
    # now I have to create transactions
    print "Start transactions creation."
    if settings.NUMBER_OF_TRANSACTIONS > 0:
        transactions = create_transactions(list_instances, connections, list_context)
        # write neo4j queries to represent those transactions
        neoManager.neo4j_add_transactions(transactions)
    print "Transactions creation completed."


def print_neo4j_queries():
    print "Started to write queries on db."
    write_file.write_to_file(neoManager)
    print "File ready to be loaded."


def adjust_communities():
    if settings.ADJUST_COMMUNITIES:
        neoManager.adjust_communities()


def delete_isolated_nodes():
    if settings.DELETE_ISOLATED_NODES:
        neoManager.neo4j_delete_isolated_nodes()


if __name__ == "__main__":
    # read data useful to create nodes
    utilities.print_date("started")
    print "Read and prepare to create dataset"
    readFile = ReadFile.ReadFile()
    neoManager = Neo4JManager.Neo4JManager()
    context = prepare_environment()
    objects, instances = prepare_nodes()
    connections = prepare_nodes_connections(objects, readFile.travel_distances)
    delete_isolated_nodes()
    adjust_communities()
    prepare_transactions(instances, connections, context)
    print_neo4j_queries()
    utilities.print_date("ended")
