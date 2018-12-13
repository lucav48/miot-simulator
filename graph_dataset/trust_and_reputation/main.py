from graph_dataset.trust_and_reputation.neo4jHandler import Neo4JManager
from tools import Tools
import settings
import random
import time

trust_repository = {}
maxNumTranSet = {}
maxSize = {}


def create_transactions(neo, instances):
    list_transactions = {}
    list_context = Tools.read_context_list()
    for i in range(0, settings.NUMBER_OF_TRANSACTIONS):
        start_instance = random.choice(instances).code
        final_instance = select_destination(start_instance)
        # put order in list_transactions
        if (final_instance, start_instance) in list_transactions:
            app = start_instance
            start_instance = final_instance
            final_instance = app
        # get context
        context = Tools.choose_context(list_context, list_transactions, start_instance, final_instance)
        # get format and size
        file_format, size = Tools.choose_transaction_format_and_size()
        trust_instances = \
            compute_trust_between_instances(start_instance, final_instance, context, file_format, size, list_transactions)
        if trust_instances > settings.LIMIT_TRUST_TO_HAVE_A_TRANSACTION:
            # if start and finish are in the correct order
            if (start_instance, final_instance) in list_transactions:
                if (context, file_format) in list_transactions[(start_instance, final_instance)]:
                    list_transactions[(start_instance, final_instance)][(context, file_format)].append(
                      neo.generate_transaction(i, start_instance, final_instance, context, file_format, size))
                else:
                    list_transactions[(start_instance, final_instance)][(context, file_format)] = \
                        [neo.generate_transaction(i, start_instance, final_instance, context, file_format, size)]

            # if instances never had a transaction
            else:
                list_transactions[(start_instance, final_instance)] = {}
                list_transactions[(start_instance, final_instance)][(context, file_format)] = \
                    [neo.generate_transaction(i, start_instance, final_instance, context, file_format, size)]
            update_maxsize_and_maxnumtranset(size, context, file_format)
        else:
            # TODO CALCOLO REPUTATION
            print "reputation"
            rep = compute_instance_reputation_in_an_IoT(final_instance, context, file_format, size, list_transactions)
    return list_transactions


def compute_instance_reputation_in_an_IoT(instance, context, file_format, size, list_transactions):
    # transactions in which "instance" compares
    transactions_to_watch = [(x, y) for (x, y) in list_transactions
                             if (x == instance or y == instance) and
                             (context, file_format) in list_transactions[(x, y)]]
    for ()



def compute_trust_between_instances(start_instance, final_instance, context, file_format, size, list_transactions):
    # if instances have never communicated before
    if (start_instance, final_instance) not in list_transactions:
        trust_repository[(start_instance, final_instance)] = {}

    if (context, file_format) not in trust_repository[(start_instance, final_instance)]:
        trust_repository[(start_instance, final_instance)][(context, file_format)] = settings.INITIAL_TRUST_VALUE
        trust_instances = settings.INITIAL_TRUST_VALUE
    else:
        transactions_to_watch = list_transactions[(start_instance, final_instance)][(context, file_format)]
        success_number = Tools.count_transaction_parameter(transactions_to_watch, "success", 1)
        success_fraction = success_number / float(len(transactions_to_watch))
        actual_max_num_tran_set = maxNumTranSet[(context, file_format)]
        actual_max_size = maxSize[(context, file_format)]
        transet_ratio = len(transactions_to_watch) / float(actual_max_num_tran_set)
        size_ratio = size/float(actual_max_size)
        trust_instances = (settings.ALPHA * success_fraction + settings.BETA * transet_ratio +
                           settings.GAMMA * size_ratio) / \
                          (settings.ALPHA + settings.BETA + settings.GAMMA)
        trust_repository[(start_instance, final_instance)][context, file_format] = trust_instances

    return trust_instances


def update_maxsize_and_maxnumtranset(new_size, context, file_format):
    if (context, file_format) not in maxNumTranSet:
        maxNumTranSet[(context, file_format)] = 1
    else:
        maxNumTranSet[(context, file_format)] = maxNumTranSet[(context, file_format)] + 1

    if (context, file_format) not in maxSize:
        maxSize[(context, file_format)] = new_size
    else:
        if new_size > maxSize[(context, file_format)]:
            maxSize[(context, file_format)] = new_size


def select_destination(start_instance):
    linked_instances_code = neo.get_instances_linked_to(start_instance)
    destination = random.choice(linked_instances_code)["code"]
    while destination == start_instance:
        destination = random.choice(linked_instances_code)["code"]
    return destination


if __name__ == "__main__":
    neo = Neo4JManager.Neo4JManager()
    instances = neo.read_instances()
    transactions = create_transactions(neo, instances)
    print ""
