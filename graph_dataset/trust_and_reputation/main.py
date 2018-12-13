from graph_dataset.trust_and_reputation.neo4jHandler import Neo4JManager
from tools import Tools
import settings
import random

trust_repository = {}


def create_transactions(neo, instances):
    list_transactions = {}
    list_context = Tools.read_context_list()
    for i in range(0, settings.NUMBER_OF_TRANSACTIONS):
        start_instance = random.choice(instances).code
        final_instance = select_destination(start_instance)
        compute_trust_and_reputation(start_instance, final_instance)
        context = Tools.choose_context(list_context, list_transactions, start_instance, final_instance)
        # if start and finish are in the correct order
        if (start_instance, final_instance) in list_transactions:
            list_transactions[(start_instance, final_instance)].append(
                neo.generate_transaction(i, start_instance, final_instance, context))
        # if start and finish are in the wrong order
        elif (final_instance, start_instance) in list_transactions:
            list_transactions[(final_instance, start_instance)].append(
                neo.generate_transaction(i, start_instance, final_instance, context))
        # if instances never had a transaction
        else:
            list_transactions[(start_instance, final_instance)] = \
                [neo.generate_transaction(i, start_instance, final_instance, context)]
    return list_transactions

def compute_trust_and_reputation(start_instance, final_instance):
    # TODO il trust va messo qua per decidere con quali instanze collaborare


def select_destination(start_instance):
    linked_instances_code = neo.get_instances_linked_to(start_instance)
    return random.choice(linked_instances_code)["code"]


if __name__ == "__main__":
    neo = Neo4JManager.Neo4JManager()
    instances = neo.read_instances()
    transactions = create_transactions(neo, instances)
    print ""
