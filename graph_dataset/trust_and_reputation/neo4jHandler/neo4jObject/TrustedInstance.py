from graph_dataset.create_dataset.neo4JHandler.neo4JObject.Instance import Instance
from graph_dataset.trust_and_reputation import settings
import random


class TrustedInstance(Instance):

    def __init__(self, i, selected_as_trust_repository):
        Instance.__init__(self, "", i["code"], i["community"])
        self.trust_repository = selected_as_trust_repository
        self.precision_instance = self.get_precision_instance()
        # self.failure_rate_object = round(uniform(settings.PERCENTAGE_FAILURE_TRANSACTIONS_OBJECT[0],
        #                                         settings.PERCENTAGE_FAILURE_TRANSACTIONS_OBJECT[1]), 3)

    def get_precision_instance(self):
        pos = random.choice(range(0, len(settings.OBJECTS)))
        while settings.OBJECTS[pos] == 0:
            pos = random.choice(range(0, len(settings.OBJECTS)))
        settings.OBJECTS[pos] -= 1
        if pos == 0:
            return round(random.uniform(0, 0.1), 3)
        elif pos == 1:
            return round(random.uniform(0.45, 0.55), 3)
        elif pos == 2:
            return round(random.uniform(0.85, 0.95), 3)
