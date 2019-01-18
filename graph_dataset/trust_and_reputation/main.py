from neo4jHandler import Neo4JManager
from computation_core import TrustComputation
from computation_core import ReputationComputation
from computation_core import TransactionsComputation
from tools import Tools
from tools import Performance
import settings
import random


def create_transactions(neo, transactionComputation, trustComputation, reputationComputation):
    list_context = Tools.read_context_list()
    i = 0
    j = 0
    while i < settings.NUMBER_OF_TRANSACTIONS:
        start_instance = random.choice(neo.list_instances.values())
        final_instance = select_destination(start_instance.code)
        context = Tools.choose_context(list_context, transactionComputation.list_transactions, start_instance.code, final_instance.code)
        # get format and size
        file_format, size = Tools.choose_transaction_format_and_size()
        trust_instances = \
            round(trustComputation.compute_trust_instances(start_instance.code, final_instance.code, context,
                                                           file_format, size, start_instance.community), 3)
        trust_instances = compute_resilience_system(neo.resilience_system_nodes, trust_instances, start_instance.code)
        have_transaction = False
        if trust_instances < settings.LIMIT_TRUST_TO_HAVE_A_TRANSACTION:
            j += 1
            reputation = reputationComputation.compute_reputation_instance(start_instance.code,
                                                                           start_instance.community,
                                                                           context, file_format)
            reputation = compute_resilience_system(neo.resilience_system_nodes, reputation, start_instance.code)
            if reputation > settings.LIMIT_REPUTATION_TO_HAVE_A_TRANSACTION:
                have_transaction = True
        else:
            have_transaction = True

        if have_transaction:
            transactionComputation.add_new_transaction(i, start_instance, final_instance, context,
                                                       file_format, size)
            i += 1
    print "Reputation computed for ", j, " iterations."
    print "Transaction creation completed."


def compute_resilience_system(resilience_nodes, previous_value, instance_code):
    if settings.COMPUTE_SYSTEM_RESILIENCE and instance_code in resilience_nodes:
        return settings.RESILIENCE_VALUE
    else:
        return previous_value


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


if __name__ == "__main__":
    print "Script started."
    print "Setup environment.."
    print "-" * 100
    print "Parameters of simulation"
    print "Number of transactions: ", settings.NUMBER_OF_TRANSACTIONS
    print "Damping factor: ", settings.DAMPING_FACTOR
    print "Alpha: ", settings.ALPHA
    print "Beta: ", settings.BETA
    print "Gamma: ", settings.GAMMA
    print "Damping factor reputation: ", settings.DAMPING_FACTOR_REPUTATION
    print "-" * 100
    performance, neo, transactionComputation, trustComputation, reputationComputation = get_instance_classes()
    performance.set_start_ts()
    print "Creating transactions..."
    create_transactions(neo, transactionComputation, trustComputation, reputationComputation)
    print "Script finished."
    performance.calculate_execution_time()
    performance.mean_values(trustComputation.mean_trust)
    # performance.mean_values(reputationComputation.mean_reputation)
    performance.statistics(transactionComputation.list_transactions)
    # performance.print_trust(trust_repository)
    # performance.plot_values(reputationComputation.reputation_repository)
    # performance.list_network_trusts(trustComputation, reputationComputation)
