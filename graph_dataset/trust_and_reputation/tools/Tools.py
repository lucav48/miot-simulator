from graph_dataset.create_dataset import settings as create_settings
from graph_dataset.trust_and_reputation import settings
import os
import random


def read_context_list():
    context = []
    files = os.listdir("../create_dataset/metadata/context")
    for f in files:
        context.append(f.replace(create_settings.SUFFIX_CONTEXT_FILE, ""))
    return context


def choose_context(list_context, list_transactions, start_instance, final_instance):
    if (start_instance, final_instance) in list_transactions:
        transactions_to_watch = list_transactions[(start_instance, final_instance)]
    elif (final_instance, start_instance) in list_transactions:
        transactions_to_watch = list_transactions[(final_instance, start_instance)]
    else:
        return random.choice(list_context)
    harvest_context = []
    for tran in transactions_to_watch:
        if tran.context not in harvest_context:
            harvest_context.append(tran.context)
    if random.random() < settings.PROBABILITY_TO_CHOOSE_FROM_CONTEXT_ALREADY_USED:
        return random.choice(harvest_context)
    else:
        return random.choice(list_context)