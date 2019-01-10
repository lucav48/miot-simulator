from graph_dataset.trust_and_reputation import settings
from graph_dataset.trust_and_reputation.tools import Tools
import time


class ReputationComputation:

    def __init__(self, neo, transaction_computation_instance, trust_computation_instance):
        self.neo = neo
        self.transaction_core = transaction_computation_instance
        self.trust_core = trust_computation_instance
        self.reputation_repository = {}
        self.max_reputation_community = {}
        self.reputation_repository = {}
        self.reputation_object = {}
        self.reputation_iot = {}
        self.max_reputation_community = {}
        self.setup_parameters()

    def setup_parameters(self):
        for i in range(1, self.neo.number_of_communities + 1):
            self.reputation_repository[str(i)] = {}
            self.max_reputation_community[str(i)] = 1.

    def compute_reputation_instance(self, ins, community, context, file_format):
        self.compute_reputation_instances_iot(str(community), context, file_format)
        # print reputation_repository
        return self.reputation_repository[community][ins][(context, file_format)]

    def compute_reputation_instances_iot(self, community, context, file_format):
        list_transactions = self.transaction_core.list_transactions
        instances_iot = self.neo.get_instances_from_community(community)
        reputation_vector = {}
        for instance in instances_iot:
            if instance in self.reputation_repository[community]:
                if (context, file_format) in self.reputation_repository[community][instance]:
                    reputation_vector[instance] = self.reputation_repository[community][instance][(context,
                                                                                                   file_format)]
                else:
                    reputation_vector[instance] = settings.INITIAL_REPUTATION_PAGERANK
            else:
                reputation_vector[instance] = settings.INITIAL_REPUTATION_PAGERANK

        current_ts = time.time()
        while True:
            new_reputation = {}
            for instance in instances_iot:
                behavioral_neighborhood = Tools.get_behavioral_neighborhood(instance, instances_iot,
                                                                            context, file_format, list_transactions)
                if behavioral_neighborhood:
                    sum_behavioral = 0.
                    for final_instance in behavioral_neighborhood:
                        # get value from trust_repository
                        trust = self.trust_core.get_trust_instances(final_instance, instance, context, file_format)
                        rep = reputation_vector[final_instance]
                        ts_ratio = self.transaction_core.first_ts[instance] / current_ts
                        ts = 1 - ts_ratio
                        sum_behavioral = sum_behavioral + (trust * rep * ts)
                    mean_behavioral = sum_behavioral / len(behavioral_neighborhood)
                    new_reputation[instance] = mean_behavioral
                else:
                    new_reputation[instance] = reputation_vector[instance]
            # max di new_reputation
            max_value = max(new_reputation.values())
            if max_value == 0:
                max_value = 1.
            # normalize
            for instance in new_reputation:
                new_reputation[instance] = new_reputation[instance] / max_value
                new_reputation[instance] = settings.GAMMA + (1 - settings.GAMMA) * new_reputation[instance]
            # get another max
            max_new_reputation = 0.
            for instance in new_reputation:
                if new_reputation[instance] > max_new_reputation and \
                        new_reputation[instance] != settings.INITIAL_REPUTATION_PAGERANK:
                    max_new_reputation = new_reputation[instance]
            # re normalize
            max_rep_community = max(self.max_reputation_community.values())
            if max_rep_community == 0:
                max_rep_community = 1.
            for instance in new_reputation:
                new_reputation[instance] = (new_reputation[instance]) * (max_new_reputation / max_rep_community)
            self.max_reputation_community[community] = max_new_reputation
            if Tools.is_converging(new_reputation, reputation_vector):
                reputation_vector = new_reputation
                break
            else:
                reputation_vector = new_reputation
        self.update_reputation_repository(community, reputation_vector, context, file_format)

    def update_reputation_repository(self, community, reputation_vector, context, file_format):
        for instance in reputation_vector:
            if instance not in self.reputation_repository[community]:
                self.reputation_repository[community][instance] = {}
            self.reputation_repository[community][instance][(context, file_format)] = reputation_vector[instance]

    def compute_reputation_iot_in_miot(self):
        number_of_communities = self.neo.number_of_communities
        occurrences = {}
        objects_with_instances = self.neo.objects_with_instances
        for i in range(1, number_of_communities + 1):
            self.reputation_iot[str(i)] = {}
            occurrences[str(i)] = {}
        for obj in objects_with_instances:
            list_instances = objects_with_instances[obj]
            for instance in list_instances:
                instance_community = self.neo.get_community_from_instance(instance)
                for c_f_f in self.reputation_object[obj]:
                    if c_f_f not in self.reputation_iot[instance_community]:
                        self.reputation_iot[instance_community][c_f_f] = 0.
                        occurrences[instance_community][c_f_f] = 0
                        self.reputation_iot[instance_community][c_f_f] = self.reputation_iot[instance_community][c_f_f] + \
                                                                         self.reputation_object[obj][c_f_f]
                    occurrences[instance_community][c_f_f] = occurrences[instance_community][c_f_f] + 1
        for community in self.reputation_iot:
            for c_f_f in self.reputation_iot[community]:
                self.reputation_iot[community][c_f_f] = self.reputation_iot[community][c_f_f] / occurrences[community][c_f_f]

    def compute_reputation_objects_in_miot(self):
        list_objects = self.neo.objects_with_instances
        actual_reputation = {}
        new_reputation = {}
        for obj in list_objects:
            actual_reputation[obj] = {}
            new_reputation[obj] = {}
        while True:
            for obj in list_objects:
                obj_instances = list_objects[obj]
                mean_values = {}
                occurrences = {}
                for instance in obj_instances:
                    behavioral_neighborhood = Tools.get_behavioral_neighborhood_from_path(instance,
                                                                                          self.trust_core.trust_repository.keys())
                    for neighbor in behavioral_neighborhood:
                        if (neighbor, instance) in self.trust_core.trust_repository:
                            for (context, file_format) in self.trust_core.trust_repository[(neighbor, instance)]:
                                neighbor_object = neighbor.split(":")[0]
                                if (context, file_format) not in mean_values:
                                    mean_values[(context, file_format)] = 0.
                                    occurrences[(context, file_format)] = 0
                                if (context, file_format) not in actual_reputation[neighbor_object]:
                                    actual_reputation[neighbor_object][
                                        (context, file_format)] = settings.INITIAL_REPUTATION_PAGERANK
                                mean_values[(context, file_format)] = mean_values[(context, file_format)] + \
                                                                      self.trust_core.trust_repository[(neighbor, instance)][
                                                                          (context, file_format)] * \
                                                                      actual_reputation[neighbor_object][
                                                                          (context, file_format)]
                                occurrences[(context, file_format)] = occurrences[(context, file_format)] + 1
                for (context, file_format) in mean_values:
                    mean_values[(context, file_format)] = settings.DAMPING_FACTOR + \
                                                          (1 - settings.DAMPING_FACTOR) * (
                                                                      mean_values[(context, file_format)] /
                                                                      (occurrences[(context, file_format)] * len(
                                                                          obj_instances)))
                new_reputation[obj] = mean_values
            if Tools.is_converging(new_reputation, actual_reputation):
                break
            else:
                actual_reputation = new_reputation
        # get max
        max_values = {}
        for obj in new_reputation:
            for context_file_format in new_reputation[obj]:
                if context_file_format not in max_values:
                    max_values[context_file_format] = 0.
                if max_values[context_file_format] < new_reputation[obj][context_file_format]:
                    max_values[context_file_format] = new_reputation[obj][context_file_format]
        # normalize
        for obj in new_reputation:
            for context_file_format in new_reputation[obj]:
                new_reputation[obj][context_file_format] = new_reputation[obj][context_file_format] / \
                                                           max_values[context_file_format]
        self.reputation_object = new_reputation
