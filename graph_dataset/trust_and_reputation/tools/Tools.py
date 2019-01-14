from graph_dataset.create_dataset import settings as create_settings
from graph_dataset.trust_and_reputation import settings
import os
import random

graphs = {}


def read_context_list():
    context = []
    files = os.listdir("../create_dataset/metadata/context")
    for f in files:
        if f.endswith(".xml"):
            context.append(f.replace(create_settings.SUFFIX_CONTEXT_FILE, ""))
    return context


def choose_context(list_context, list_transactions, start_instance, final_instance):
    if (start_instance, final_instance) in list_transactions:
        transactions_to_watch = list_transactions[(start_instance, final_instance)]
    else:
        return random.choice(list_context)
    harvest_context = []
    for (context, _) in transactions_to_watch:
        if context not in harvest_context:
            harvest_context.append(context)
    if random.random() < settings.PROBABILITY_TO_CHOOSE_FROM_CONTEXT_ALREADY_USED:
        return random.choice(harvest_context)
    else:
        return random.choice(list_context)


def choose_transaction_format_and_size():
    file_format, range_size = random.choice(settings.FORMAT_AVAILABLES_AND_SIZE)
    return file_format, random.randint(range_size[0], range_size[1])


def count_transaction_parameter(list_transactions, parameter, value):
    count = 0
    for transaction in list_transactions:
        if getattr(transaction, parameter) == value:
            count += 1
    return count


def get_first_timestamp_in_list_transactions(list_transactions):
    first_timestamp = 10e100
    for t in list_transactions:
        if t.timestamp < first_timestamp:
            first_timestamp = t.timestamp
    return first_timestamp


def is_the_same_object(ins1, ins2):
    object1 = ins1.split(":")[0]
    object2 = ins2.split(":")[0]
    if object1 == object2:
        return True
    else:
        return False


def get_transactions_from_instance_same_network(neo, ins, context, file_format, list_transactions):
    transactions = {}
    for (start_instance, final_instance) in list_transactions:
        if start_instance == ins and (context, file_format) in list_transactions[(start_instance, final_instance)]:
            if neo.check_behavioral_neighbors(start_instance, final_instance):
                transactions[(start_instance, final_instance)] = \
                    list_transactions[(start_instance, final_instance)][(context, file_format)]
    return transactions


def get_behavioral_neighborhood_in(start_instance, linked_instances, context, file_format, list_transactions):
    behavioral_neighborhood = []
    for final_instance in linked_instances:
        if (final_instance, start_instance) in list_transactions:
            if (context, file_format) in list_transactions[(final_instance, start_instance)]:
                behavioral_neighborhood.append(final_instance)
    return behavioral_neighborhood


def linked_by_strange_path(neo, start_instance, final_instance):
    shortest_path = neo.get_shortest_path_instances(start_instance, final_instance)
    start_community = neo.get_community_from_instance(start_instance)
    final_community = neo.get_community_from_instance(final_instance)
    if start_community == final_community and len(shortest_path) > 1:
        return True
    else:
        return False


def is_converging(d1, d2):
    for key in d1:
        if abs(d1[key] - d2[key]) > settings.CONVERGENCE_PAGERANK:
            return False
    return True


def get_behavioral_neighborhood_from_path(ins, pairwise_instances):
    neighborhood = []
    for (start_instance, final_instance) in pairwise_instances:
        if ins == final_instance:
            neighborhood.append(start_instance)
    return neighborhood
