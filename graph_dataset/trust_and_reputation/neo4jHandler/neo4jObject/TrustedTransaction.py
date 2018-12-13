from graph_dataset.create_dataset.neo4JHandler.neo4JObject.Transaction import Transaction
from graph_dataset.trust_and_reputation import settings
import random
import time


class TrustedTransaction(Transaction):

    def __init__(self, code, source, destination, context):
        Transaction.__init__(self, code, source, destination, time.time(), context, "")
        self.success = self.check_success_transaction()
        self.format, self.size = self.add_transaction_format_and_size()

    def add_transaction_format_and_size(self):
        file_format, range_size = random.choice(settings.FORMAT_AVAILABLES_AND_SIZE)
        return file_format, random.randint(range_size[0], range_size[1])

    def check_success_transaction(self):
        if random.random() < 1 - settings.PERCENTAGE_FAILURE_TRANSACTIONS:
            return 0
        else:
            return 1
