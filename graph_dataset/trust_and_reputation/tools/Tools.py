from graph_dataset.create_dataset import settings as create_settings
from graph_dataset.trust_and_reputation import settings
import os
import random


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
    elif (final_instance, start_instance) in list_transactions:
        transactions_to_watch = list_transactions[(final_instance, start_instance)]
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


def get_first_timestamp_in_list_transactions(start_instance, final_instance, context, file_format, list_transactions):
    if (start_instance, final_instance) in list_transactions:
        transaction = list_transactions[(start_instance, final_instance)][(context, file_format)]
    else:
        transaction = list_transactions[(final_instance, start_instance)][(context, file_format)]
    first_timestamp = 10e100
    for t in transaction:
        if t.timestamp < first_timestamp:
            first_timestamp = t.timestamp
    return first_timestamp
