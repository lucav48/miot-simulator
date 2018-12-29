from graph_dataset.create_dataset.neo4JHandler.neo4JObject.Transaction import Transaction
from graph_dataset.trust_and_reputation import settings
import random
import time


class TrustedTransaction(Transaction):

    def __init__(self, code, source, destination, context, file_format, size, precision_instance):
        Transaction.__init__(self, code, source, destination, time.time(), context, "")
        self.success = self.check_success_transaction(precision_instance)
        self.file_format = file_format
        self.size = size

    def check_success_transaction(self, precision_instance):
        if random.random() < precision_instance:
            return 1
        else:
            return 0
