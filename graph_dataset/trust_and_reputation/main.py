from graph_dataset.trust_and_reputation.neo4jHandler import Neo4JManager
from tools import Tools
from tools import Performance
import settings
import random
import time

trust_repository = {}
reputation_repository = {}
first_ts = {}
maxReputation = {}
maxNumTranSet = {}
maxSize = {}
max_reputation_community = {}


def create_transactions(neo):
    list_transactions = {}
    list_context = Tools.read_context_list()
    for i in range(0, settings.NUMBER_OF_TRANSACTIONS):
        start_instance_complete = random.choice(neo.list_instances.values())
        start_instance = start_instance_complete.code
        final_instance_complete = select_destination(start_instance)
        final_instance = final_instance_complete.code
        context = Tools.choose_context(list_context, list_transactions, start_instance, final_instance)
        # get format and size
        file_format, size = Tools.choose_transaction_format_and_size()
        trust_instances = \
            round(compute_trust_instances(neo, start_instance, final_instance, context, file_format, size,
                                          start_instance_complete.community, list_transactions), 3)
        update_trust_repository(start_instance, final_instance, context, file_format, trust_instances)
        have_transaction = False
        if trust_instances < settings.LIMIT_TRUST_TO_HAVE_A_TRANSACTION:
            reputation = compute_reputation_instance(neo, start_instance, start_instance_complete.community,
                                                     context, file_format, list_transactions)
            if reputation > settings.LIMIT_REPUTATION_TO_HAVE_A_TRANSACTION:
                have_transaction = True
        else:
            have_transaction = True

        if have_transaction:
            list_transactions, success_transaction = add_new_transaction(i, start_instance, final_instance, context,
                                                                         file_format, size,
                                                                         final_instance_complete.precision_instance,
                                                                         list_transactions)
            update_maxsize_and_maxnumtranset(size, context, file_format, start_instance_complete.community,
                                             success_transaction)
    return list_transactions


def compute_reputation_instance(neo, ins, community, context, file_format, list_transactions):
    compute_reputation_instances_iot(neo, str(community), context, file_format, list_transactions)
    # print reputation_repository
    return reputation_repository[community][ins][(context, file_format)]


def compute_reputation_instances_iot(neo, community, context, file_format, list_transactions):
    instances_iot = neo.get_instances_from_community(community)
    reputation_vector = {}
    for instance in instances_iot:
        if instance in reputation_repository[community]:
            if (context, file_format) in reputation_repository[community][instance]:
                reputation_vector[instance] = reputation_repository[community][instance][(context, file_format)]
            else:
                reputation_vector[instance] = settings.INITIAL_REPUTATION_PAGERANK
        else:
            reputation_vector[instance] = settings.INITIAL_REPUTATION_PAGERANK

    current_ts = time.time()
    while True:
        new_reputation = {}
        for instance in instances_iot:
            behavioral_neighborhood = Tools.get_behavioral_neighborhood(instance, instances_iot,
                                                                        context, file_format, list_transactions)
            if behavioral_neighborhood:
                sum_behavioral = 0.
                for final_instance in behavioral_neighborhood:
                    # get value from trust_repository
                    trust = get_trust_instances(final_instance, instance, context, file_format)
                    rep = reputation_vector[final_instance]
                    ts_ratio = first_ts[instance] / current_ts
                    ts = 1 - ts_ratio
                    sum_behavioral = sum_behavioral + (trust * rep)
                mean_behavioral = sum_behavioral / len(behavioral_neighborhood)
                # rep_score = settings.DAMPING_FACTOR + (1 - settings.DAMPING_FACTOR) * mean_behavioral
                new_reputation[instance] = mean_behavioral
            else:
                new_reputation[instance] = reputation_vector[instance]
        # max di new_reputation
        max_value = max(new_reputation.values())
        # normalize
        for instance in new_reputation:
            new_reputation[instance] = new_reputation[instance] / max_value
            new_reputation[instance] = settings.GAMMA + (1 - settings.GAMMA) * new_reputation[instance]
        # get another max
        max_new_reputation = 0.
        for instance in new_reputation:
            if new_reputation[instance] > max_new_reputation and new_reputation[instance] != 1:
                max_new_reputation = new_reputation[instance]
        # re normalize
        for instance in new_reputation:
            new_reputation[instance] = (new_reputation[instance]) * (max_new_reputation /
                                                                     max(max_reputation_community.values()))
        max_reputation_community[community] = max_new_reputation
        if is_converging(new_reputation, reputation_vector):
            reputation_vector = new_reputation
            break
        else:
            reputation_vector = new_reputation
    update_reputation_repository(community, reputation_vector, context, file_format)


def get_trust_instances(ins_start, ins_finish, context, file_format):
    found = False
    trust = settings.INITIAL_TRUST_VALUE
    if (ins_finish, ins_start) in trust_repository:
        if (context, file_format) in trust_repository[(ins_finish, ins_start)]:
            found = True
            trust = trust_repository[(ins_finish, ins_start)][(context, file_format)]
    if not found:
        trust_repository[(ins_finish, ins_start)][(context, file_format)] = trust
    return trust


def update_reputation_repository(community, reputation_vector, context, file_format):
    max_reputation = 0.
    for instance in reputation_vector:
        if instance not in reputation_repository[community]:
            reputation_repository[community][instance] = {}
        if reputation_vector[instance] > max_reputation:
            max_reputation = reputation_vector[instance]

    for instance in reputation_vector:
        rep_score = reputation_vector[instance]
        reputation_repository[community][instance][(context, file_format)] = rep_score

    #     if reputation_vector[instance] > max_reputation:
    #         max_reputation = reputation_vector[instance]
    # for instance in reputation_vector:
    #     rep_score = reputation_vector[instance] #/ max_reputation
    #     if instance not in reputation_repository[community]:
    #         reputation_repository[community][instance] = {}
    #     reputation_repository[community][instance][(context, file_format)] = rep_score


def is_converging(d1, d2):
    for key in d1:
        if abs(d1[key] - d2[key]) > settings.CONVERGENCE_PAGERANK:
            return False
    return True


def compute_trust_instances(neo, start_instance, final_instance, context, file_format,
                            size, community, list_transactions):
    # check which trust score to compute
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
                trust_score = compute_trust_instance_different_network(shortest_path, context, file_format, size,
                                                                       community, list_transactions)
            return trust_score


def compute_trust_instances_same_network(start_instance, final_instance, context, file_format, size, community, list_transactions):
    # if instances have never communicated before
    transactions_to_watch = list_transactions[(start_instance, final_instance)][(context, file_format)]
    success_number = 0
    for t in transactions_to_watch:
        if t.success == 1:
            success_number += 1
    success_fraction = success_number / float(len(transactions_to_watch))
    if (context, file_format) not in maxNumTranSet[community]:
        transet_fraction_den = 1.
    else:
        transet_fraction_den = float(maxNumTranSet[community][(context, file_format)])
    transet_fraction = len(transactions_to_watch) / transet_fraction_den
    size_fraction = size / float(maxSize[community][(context, file_format)])
    trust_score = (settings.ALPHA * success_fraction +
                   settings.BETA * transet_fraction +
                   settings.GAMMA * size_fraction) / \
                  (settings.ALPHA + settings.BETA + settings.GAMMA)
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
                start_instance = start_instance["code"]
                final_instance = final_instance["code"]
                if (start_instance, final_instance) in trust_repository:
                    if (context, file_format) in trust_repository[(start_instance, final_instance)]:
                        trust_score *= trust_repository[(start_instance, final_instance)][(context, file_format)]
                    else:
                        trust_score *= compute_trust_instances_same_network(start_instance["code"],
                                                                            final_instance["code"],
                                                                            context, file_format, size,
                                                                            community, list_transactions)
                else:
                    trust_score *= compute_trust_instances_same_network(start_instance["code"], final_instance["code"],
                                                                        context, file_format, size,
                                                                        community, list_transactions)
    return trust_score


def add_new_transaction(code, start_instance, final_instance, context, file_format, size,
                        precision_instance, list_transactions):
    new_transaction = neo.generate_transaction(code, start_instance, final_instance, context, file_format,
                                               size, precision_instance)
    if (start_instance, final_instance) not in list_transactions:
        list_transactions[(start_instance, final_instance)] = {}
        list_transactions[(start_instance, final_instance)][(context, file_format)] = [new_transaction]
    else:
        if (context, file_format) not in list_transactions[(start_instance, final_instance)]:
            list_transactions[(start_instance, final_instance)][(context, file_format)] = [new_transaction]
        else:
            list_transactions[(start_instance, final_instance)][(context, file_format)].append(new_transaction)
    # update first ts
    if start_instance not in first_ts:
        first_ts[start_instance] = time.time()
    return list_transactions, new_transaction.success


def update_trust_repository(start_instance, final_instance, context, file_format, trust_instances):
    if (start_instance, final_instance) not in trust_repository:
        trust_repository[(start_instance, final_instance)] = {}
    trust_repository[(start_instance, final_instance)][(context, file_format)] = trust_instances


def update_maxsize_and_maxnumtranset(new_size, context, file_format, community, success_transaction):
    if success_transaction == 1:
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
        reputation_repository[str(i)] = {}
        max_reputation_community[str(i)] = 1.


if __name__ == "__main__":
    print "Script started."
    neo = Neo4JManager.Neo4JManager()
    print "Setup environment.."
    setup_maxnumtranset_and_maxsize(neo.number_of_communities)
    performance = Performance.Performance(neo)
    performance.set_start_ts()
    print "Creating transactions..."
    transactions = create_transactions(neo)
    print "Script finished."
    performance.calculate_execution_time()
    performance.statistics(transactions)
    print max_reputation_community
    # performance.print_trust(trust_repository)
    performance.plot_values(reputation_repository, transactions)
    print ""
