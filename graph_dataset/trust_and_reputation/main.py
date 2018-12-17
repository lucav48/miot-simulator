from graph_dataset.trust_and_reputation.neo4jHandler import Neo4JManager
from tools import Tools
import settings
import random
import time

trust_repository = {}
maxReputation = {}
maxNumTranSet = {}
maxSize = {}


def create_transactions(neo, instances):
    list_transactions = {}
    list_context = Tools.read_context_list()
    for i in range(0, settings.NUMBER_OF_TRANSACTIONS):
        start_instance_complete = random.choice(instances)
        start_instance = start_instance_complete.code
        final_instance_complete = select_destination(start_instance)
        final_instance = final_instance_complete.code
        # # put order in list_transactions
        # if (final_instance, start_instance) in list_transactions:
        #     app = start_instance
        #     start_instance = final_instance
        #     final_instance = app
        # get context
        context = Tools.choose_context(list_context, list_transactions, start_instance, final_instance)
        # get format and size
        file_format, size = Tools.choose_transaction_format_and_size()
        trust_instances = \
            round(compute_trust_instances(neo, start_instance, final_instance, context, file_format, size,
                                          start_instance_complete.community, list_transactions), 3)
        update_trust_repository(start_instance, final_instance, context, file_format, trust_instances)
        have_transaction = False
        if trust_instances < settings.LIMIT_TRUST_TO_HAVE_A_TRANSACTION:
            reputation = compute_reputation_instance(neo, final_instance_complete,
                                                     context, file_format, list_transactions, settings.DEPTH_REPUTATION)
            if reputation > settings.LIMIT_REPUTATION_TO_HAVE_A_TRANSACTION:
                have_transaction = True
        else:
            have_transaction = True

        if have_transaction:
            list_transactions = add_new_transaction(i, start_instance, final_instance, context, file_format, size,
                                                    list_transactions)
            update_maxsize_and_maxnumtranset(size, context, file_format, start_instance_complete.community)
    return list_transactions


def compute_reputation_instance(neo, instance, context, file_format, list_transactions, depth):
    if depth == 0:
        return settings.INITIAL_REPUTATION_VALUE
    current_ts = time.time()
    transactions_to_watch = Tools.get_transactions_from_instance_same_network(neo, instance, context, file_format,
                                                                              list_transactions)
    if transactions_to_watch:
        sum_partial_reputation = 0.
        for (start_instance, final_instance) in transactions_to_watch:
            # check which instance I am
            if start_instance == instance.code:
                other_instance = neo.get_instance_from_code(final_instance)
            else:
                other_instance = neo.get_instance_from_code(start_instance)
            # get first timestamp
            first_ts = Tools.get_first_timestamp_in_list_transactions(
                transactions_to_watch[(start_instance, final_instance)])
            reputation_other_instance = compute_reputation_instance(neo, other_instance, context, file_format,
                                                                    list_transactions, depth-1)
            trust_between_instances = trust_repository[(start_instance, final_instance)][(context, file_format)]
            sum_partial_reputation += trust_between_instances * reputation_other_instance * \
                                      (1 - (first_ts/current_ts))
        reputation_relative = settings.DUMPING_FACTOR + (1 - settings.DUMPING_FACTOR) * sum_partial_reputation / \
                              len(transactions_to_watch)
        reputation = reputation_relative / maxReputation[instance.community]
        if reputation > maxReputation[instance.community]:
            maxReputation[instance.community] = reputation
        return round(reputation, 3)
    else:
        return settings.INITIAL_REPUTATION_VALUE


def compute_trust_instances(neo, start_instance, final_instance, context, file_format, size, community, list_transactions):
    # check which trust score to compute
    neo.get_shortest_path_instances(start_instance, final_instance)
    if (start_instance, final_instance) not in list_transactions:
        return settings.INITIAL_TRUST_VALUE
    else:
        # if there is no transaction with those context and file format, it returns the initial trust value
        if (context, file_format) not in list_transactions[(start_instance, final_instance)]:
            return settings.INITIAL_TRUST_VALUE
        else:
            # check if instances are in the same network
            if neo.object_in_the_same_network(start_instance, final_instance):
                trust_score = compute_trust_instances_same_network(start_instance, final_instance, context, file_format,
                                                                   size, community, list_transactions)
            else:
                shortest_path = neo.get_shortest_path_instances(start_instance, final_instance)
                trust_score = compute_trust_instance_different_network(shortest_path, context,
                                                                       file_format, size, community, list_transactions)
            return trust_score


def compute_trust_instances_same_network(start_instance, final_instance, context, file_format, size, community, list_transactions):
    # if instances have never communicated before
    transactions_to_watch = list_transactions[(start_instance, final_instance)][(context, file_format)]
    success_number = 0
    for t in transactions_to_watch:
        if t.success == 1:
            success_number += 1
    success_fraction = success_number / float(len(transactions_to_watch))
    transet_fraction = len(transactions_to_watch) / \
                       float(maxNumTranSet[community][(context, file_format)])
    size_fraction = size / float(maxSize[community][(context, file_format)])
    trust_score = (settings.ALPHA * success_fraction +
                   settings.BETA * transet_fraction +
                   settings.GAMMA * size_fraction) / (settings.ALPHA + settings.BETA + settings.GAMMA)
    return trust_score


def compute_trust_instance_different_network(shortest_path, context, file_format, size, community, list_transactions):
    trust_score = 1.
    for (start_instance, final_instance) in shortest_path:
        if (start_instance, final_instance) not in list_transactions:
            trust_score *= settings.INITIAL_TRUST_VALUE
        else:
            if (context, file_format) not in list_transactions:
                trust_score *= settings.INITIAL_TRUST_VALUE
            else:
                trust_score *= compute_trust_instances_same_network(start_instance["code"], final_instance["code"],
                                                                    context, file_format, size,
                                                                    community, list_transactions)
    return trust_score


def add_new_transaction(code, start_instance, final_instance, context, file_format, size, list_transactions):
    if (start_instance, final_instance) not in list_transactions:
        list_transactions[(start_instance, final_instance)] = {}
        list_transactions[(start_instance, final_instance)][(context, file_format)] = [
            neo.generate_transaction(code, start_instance, final_instance, context, file_format, size)]
    else:
        if (context, file_format) not in list_transactions[(start_instance, final_instance)]:
            list_transactions[(start_instance, final_instance)][(context, file_format)] = [
                neo.generate_transaction(code, start_instance, final_instance, context, file_format, size)]
        else:
            list_transactions[(start_instance, final_instance)][(context, file_format)].append(
                neo.generate_transaction(code, start_instance, final_instance, context, file_format, size))

    return list_transactions


def update_trust_repository(start_instance, final_instance, context, file_format, trust_instances):
    if (start_instance, final_instance) not in trust_repository:
        trust_repository[(start_instance, final_instance)] = {}
    trust_repository[(start_instance, final_instance)][(context, file_format)] = trust_instances


def update_maxsize_and_maxnumtranset(new_size, context, file_format, community):
    if (context, file_format) not in maxNumTranSet[community]:
        maxNumTranSet[community][(context, file_format)] = 1
    else:
        maxNumTranSet[community][(context, file_format)] = maxNumTranSet[community][(context, file_format)] + 1

    if (context, file_format) not in maxSize[community]:
        maxSize[community][(context, file_format)] = new_size
    else:
        if new_size > maxSize[community][(context, file_format)]:
            maxSize[community][(context, file_format)] = new_size


def select_destination(start_instance):
    linked_instances_code = neo.get_instances_linked_to(start_instance)
    destination_instance = random.choice(linked_instances_code)
    while destination_instance.code == start_instance or \
            Tools.is_the_same_object(start_instance, destination_instance.code):
        destination_instance = random.choice(linked_instances_code)
    return destination_instance


def setup_maxnumtranset_and_maxsize(number_of_communities):
    for i in range(1, number_of_communities + 1):
        maxNumTranSet[str(i)] = {}
        maxSize[str(i)] = {}
        maxReputation[str(i)] = settings.INITIAL_REPUTATION_VALUE


if __name__ == "__main__":
    neo = Neo4JManager.Neo4JManager()
    setup_maxnumtranset_and_maxsize(neo.number_of_communities)
    instances = neo.read_instances()
    transactions = create_transactions(neo, instances)
    print ""
