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
        context = Tools.choose_context(list_context, transactionComputation.list_transactions, start_instance.code, final_instance.code)
        # get format and size
        file_format, size = Tools.choose_transaction_format_and_size()
        trust_instances = round(trustComputation.compute_trust_instances(start_instance.code, final_instance.code,
                                                                         context, file_format, size,
                                                                         start_instance.community), 3)
        have_transaction = False
        if trust_instances < settings.LIMIT_TRUST_TO_HAVE_A_TRANSACTION:
            j += 1
            reputation = reputationComputation.compute_reputation_instance(start_instance.code,
                                                                           start_instance.community,
                                                                           context, file_format)
            if reputation > settings.LIMIT_REPUTATION_TO_HAVE_A_TRANSACTION:
                have_transaction = True
        else:
            have_transaction = True

        if have_transaction:
            transactionComputation.add_new_transaction(i, start_instance, final_instance, context,
                                                       file_format, size)
            i += 1
            get_snapshot(i)
    print "Reputation computed for ", j, " iterations."
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
        print "TRUST INSTANCES MEAN VALUES"
        performance.mean_historical_values(trustComputation.mean_trust)
        print "-" * 100
        print "REPUTATION INSTANCES MEAN VALUES"
        performance.mean_historical_values(reputationComputation.mean_reputation)
        print "-" * 100
        trustComputation.compute_trust_objects()
        reputationComputation.compute_reputation_objects_in_miot()
        reputationComputation.compute_reputation_iot_in_miot()
        print "TRUST OBJECTS"
        performance.mean_values(trustComputation.trust_object)
        print "-" * 100
        print "REPUTATION OBJECTS"
        performance.mean_values(reputationComputation.reputation_object)
        print "-" * 100
        print "REPUTATION IOT"
        performance.mean_values(reputationComputation.reputation_iot)
        print "-" * 100


def print_simulation_parameters():
    print "Parameters of simulation"
    print "Number of transactions to create: ", settings.NUMBER_OF_TRANSACTIONS
    print "Number of instances: ", neo.number_of_instances
    print "Number of communities: ", neo.number_of_communities
    print "Alpha: ", settings.ALPHA
    print "Beta: ", settings.BETA
    print "Gamma: ", settings.GAMMA
    print "Damping factor trust: ", settings.DAMPING_FACTOR_TRUST
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
