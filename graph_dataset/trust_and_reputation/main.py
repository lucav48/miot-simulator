from neo4jHandler import Neo4JManager
from computation_core import TrustComputation
from computation_core import ReputationComputation
from computation_core import TransactionsComputation
from tools import Tools
from tools import Performance
import settings
import random


def create_transactions():
    list_context = Tools.read_context_list()
    i = 0
    j = 0
    while i < settings.NUMBER_OF_TRANSACTIONS:
        start_instance = random.choice(neo.list_instances.values())
        final_instance = select_destination(start_instance.code)
        context = Tools.choose_context(list_context, transactionComputation.list_transactions, start_instance.code,
                                       final_instance.code)
        # get format and size
        file_format, size = Tools.choose_transaction_format_and_size()
        trust_instances = round(trustComputation.compute_trust_instances(start_instance.code, final_instance.code,
                                                                         context, file_format, size,
                                                                         start_instance.community), 3)
        have_transaction = False
        if trust_instances < settings.LIMIT_TRUST_TO_HAVE_A_TRANSACTION:
            j += 1
            if (j % 10) == 0:
                reputation = reputationComputation.compute_reputation_instance(final_instance.code,
                                                                               final_instance.community,
                                                                               context, file_format)
            else:
                reputation = reputationComputation.reputation_repository[final_instance.community][final_instance.code][(context, file_format)]
            if reputation > settings.LIMIT_REPUTATION_TO_HAVE_A_TRANSACTION:
                have_transaction = True
            else:
                have_transaction = True

        if have_transaction:
            transactionComputation.add_new_transaction(i, start_instance, final_instance, context,
                                                       file_format, size)
            i += 1
            get_snapshot(i)
    print "Reputation computed for ", int(j/10), " iterations."
    print "Transaction creation completed."


def select_destination(start_instance):
    linked_instances_code = neo.get_instances_linked_to(start_instance)
    destination_instance = random.choice(linked_instances_code)
    while destination_instance.code == start_instance or \
            Tools.is_the_same_object(start_instance, destination_instance.code) or \
            Tools.linked_by_strange_path(neo, start_instance, destination_instance.code):
        linked_instances_code.remove(destination_instance)
        destination_instance = random.choice(linked_instances_code)
    return destination_instance


def get_instance_classes():
    neo_instance = Neo4JManager.Neo4JManager()
    transaction_computation_instance = TransactionsComputation.TransactionsComputation(neo_instance)
    performance_instance = Performance.Performance(neo_instance)
    trust_computation_instance = TrustComputation.TrustComputation(neo_instance, transaction_computation_instance)
    reputation_computation_instance = ReputationComputation.ReputationComputation(neo_instance,
                                                                                  transaction_computation_instance,
                                                                                  trust_computation_instance)
    return performance_instance, neo_instance, transaction_computation_instance, trust_computation_instance, \
        reputation_computation_instance


def get_snapshot(iteration):
    if iteration in settings.SNAPSHOT_AT:
        print "SNAPSHOT FOR #" + str(iteration) + " TRANSACTION"
        performance.calculate_execution_time()
        instances = "TEST_500"
        index_list = str(settings.SNAPSHOT_AT.index(iteration))
        print "TRUST INSTANCES MEAN VALUES"
        # file_path = "risultati/" + "300/" + str(int(settings.RESILIENCE_VALUE)) + "/" + str(settings.PERCENTAGE_NODE_SYSTEM_RESILIENCE) + "/"
        file_path = "risultati/andamento_trust/"
        # trust_file = "300_" + str(settings.PERCENTAGE_NODE_SYSTEM_RESILIENCE) + "_" + str(iteration) + "_trust.txt"
        trust_file_instances = index_list + "_" + instances + "_" + str(iteration) + "_instances_trust.txt"
        performance.mean_historical_values(trustComputation.mean_trust, file_path + trust_file_instances)
        print "-" * 100
        print "REPUTATION INSTANCES MEAN VALUES"
        file_path = "risultati/andamento_reputation/"
        reputation_file = index_list + "_" + instances + "_" + str(iteration) + "_instances_reputation.txt"
        # reputation_file = "300_" + str(settings.PERCENTAGE_NODE_SYSTEM_RESILIENCE) + "_" + str(iteration) + "_reputation.txt"
        performance.mean_historical_values(reputationComputation.mean_reputation, file_path + reputation_file)
        print "-" * 100
        file_path = "risultati/andamento_trust/"
        trustComputation.compute_trust_objects()
        trust_file_objects = index_list + "_" + instances + "_" + str(iteration) + "_objects_trust.txt"
        reputationComputation.compute_reputation_objects_in_miot()
        reputationComputation.compute_reputation_iot_in_miot()
        print "TRUST OBJECTS"
        performance.mean_values(trustComputation.trust_object, file_path + trust_file_objects)
        print "-" * 100
        print "REPUTATION OBJECTS"
        file_path = "risultati/andamento_reputation/"
        reputation_object_file = index_list + "_" + instances + "_" + str(iteration) + "_object_reputation.txt"
        performance.mean_values(reputationComputation.reputation_object, file_path + reputation_object_file)
        print "-" * 100
        print "REPUTATION IOT"
        reputation_iot_file = index_list + "_" + instances + "_" + str(iteration) + "_iot_reputation.txt"
        performance.mean_values(reputationComputation.reputation_iot, file_path + reputation_iot_file)
        print "-" * 100


def print_simulation_parameters():
    print "Parameters of simulation"
    print "Number of transactions to create: ", settings.NUMBER_OF_TRANSACTIONS
    print "Number of instances: ", neo.number_of_instances
    print "Number of communities: ", neo.number_of_communities
    print "Alpha: ", settings.ALPHA
    print "Beta: ", settings.BETA
    print "Gamma: ", settings.GAMMA
    print "Damping factor reputation: ", settings.DAMPING_FACTOR_REPUTATION
    print "Limit trust to have a transaction: ", settings.LIMIT_TRUST_TO_HAVE_A_TRANSACTION
    print "Limit reputation to have a transaction: ", settings.LIMIT_REPUTATION_TO_HAVE_A_TRANSACTION
    print "Compute resilience: ", settings.COMPUTE_SYSTEM_RESILIENCE
    if settings.COMPUTE_SYSTEM_RESILIENCE:
        print "Percentage resilience: ", settings.PERCENTAGE_NODE_SYSTEM_RESILIENCE
        print "Resilience value: ", settings.RESILIENCE_VALUE


if __name__ == "__main__":
    print "Script started."
    print "Setup environment.."
    performance, neo, transactionComputation, trustComputation, reputationComputation = get_instance_classes()
    performance.set_start_ts()
    print "-" * 100
    print_simulation_parameters()
    print "-" * 100
    print "Creating transactions..."
    print "-" * 100
    create_transactions()
    print "Script finished."
    # performance.calculate_execution_time()
    # performance.mean_values(trustComputation.mean_trust)
    # performance.mean_values(reputationComputation.mean_reputation)
    performance.statistics(transactionComputation.list_transactions)
    # performance.plot_values(reputationComputation.reputation_repository)
    # performance.list_network_trusts(trustComputation, reputationComputation)
