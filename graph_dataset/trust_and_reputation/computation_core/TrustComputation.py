from graph_dataset.trust_and_reputation import settings


class TrustComputation:

    def __init__(self, neo, transaction_computation_instance):
        self.neo = neo
        self.trust_repository = {}
        self.trust_object = {}
        self.overall_trust_iots = {}
        self.mean_trust = {}
        self.transaction_core = transaction_computation_instance

    def compute_trust_instances(self, start_instance, final_instance, context, file_format, size, community):
        list_transactions = self.transaction_core.list_transactions
        # check which trust score to compute
        if (start_instance, final_instance) not in list_transactions:
            trust_score = settings.INITIAL_TRUST_VALUE
        else:
            # if there is no transaction with those context and file format, it returns the initial trust value
            if (context, file_format) not in list_transactions[(start_instance, final_instance)]:
                trust_score = settings.INITIAL_TRUST_VALUE
            else:
                # check if instances are in the same network
                if self.neo.object_in_the_same_network(start_instance, final_instance):
                    trust_score = self.compute_trust_instances_engine(start_instance, final_instance, context,
                                                                      file_format, size, community)
                else:
                    shortest_path = self.neo.get_shortest_path_instances(start_instance, final_instance)
                    trust_score = self.compute_trust_instance_different_network(shortest_path, context, file_format,
                                                                                size, community)
        self.update_trust_repository(start_instance, final_instance, context, file_format, trust_score)
        return trust_score

    def compute_trust_instances_engine(self, start_instance, final_instance, context, file_format, size, community):
        list_transactions = self.transaction_core.list_transactions
        # if instances have never communicated before
        transactions_to_watch = list_transactions[(start_instance, final_instance)][(context, file_format)]
        success_number = 0
        for t in transactions_to_watch:
            if t.success == 1:
                success_number += 1
        success_fraction = success_number / float(len(transactions_to_watch))
        if (context, file_format) not in self.transaction_core.maxNumTranSet[community]:
            transet_fraction_den = 1.
        else:
            transet_fraction_den = float(self.transaction_core.maxNumTranSet[community][(context, file_format)])
        transet_fraction = len(transactions_to_watch) / transet_fraction_den
        actual_max_size = float(self.transaction_core.maxSize[community][(context, file_format)])
        if size > actual_max_size:
            size_fraction = 1.
        else:
            size_fraction = size / actual_max_size
        trust_score = (settings.ALPHA * success_fraction +
                       settings.BETA * transet_fraction +
                       settings.GAMMA * size_fraction) / \
                      (settings.ALPHA + settings.BETA + settings.GAMMA)
        return trust_score

    def compute_trust_instance_different_network(self, shortest_path, context, file_format, size, community):
        list_transactions = self.transaction_core.list_transactions
        trust_score = 1.
        for (start_instance, final_instance) in shortest_path:
            if (start_instance, final_instance) not in list_transactions:
                trust_score *= settings.INITIAL_TRUST_VALUE
            else:
                if (context, file_format) not in list_transactions:
                    trust_score *= settings.INITIAL_TRUST_VALUE
                else:
                    start_instance = start_instance["code"]
                    final_instance = final_instance["code"]
                    if (start_instance, final_instance) in self.trust_repository:
                        if (context, file_format) in self.trust_repository[(start_instance, final_instance)]:
                            trust_score *= self.trust_repository[(start_instance, final_instance)][(context, file_format)]
                        else:
                            trust_score *= self.compute_trust_instances_engine(start_instance["code"],
                                                                               final_instance["code"],
                                                                               context, file_format, size, community)
                    else:
                        trust_score *= self.compute_trust_instances_engine(start_instance["code"],
                                                                           final_instance["code"],
                                                                           context, file_format, size,
                                                                           community)
        return trust_score

    def update_trust_repository(self, start_instance, final_instance, context, file_format, trust_instances):
        if (start_instance, final_instance) not in self.trust_repository:
            self.trust_repository[(start_instance, final_instance)] = {}
            self.mean_trust[(start_instance, final_instance)] = {}
        if (context, file_format) not in self.mean_trust[(start_instance, final_instance)]:
            self.mean_trust[(start_instance, final_instance)][(context, file_format)] = []
        self.trust_repository[(start_instance, final_instance)][(context, file_format)] = trust_instances
        self.mean_trust[(start_instance, final_instance)][(context, file_format)].append(trust_instances)

    def get_trust_instances(self, ins_start, ins_finish, context, file_format):
        found = False
        trust = settings.INITIAL_TRUST_VALUE
        if (ins_start, ins_finish) in self.trust_repository:
            if (context, file_format) in self.trust_repository[(ins_start, ins_finish)]:
                found = True
                trust = self.trust_repository[(ins_start, ins_finish)][(context, file_format)]
        if not found:
            if (ins_start, ins_finish) not in self.trust_repository:
                self.trust_repository[(ins_start, ins_finish)] = {}
                self.trust_repository[(ins_start, ins_finish)][(context, file_format)] = trust
        return trust

    def compute_trust_object_to_iot(self):
        trust_objects_to_iot = {}
        index_to_fill = []
        objects_with_instances = self.neo.objects_with_instances
        for obj in objects_with_instances:
            trust_objects_to_iot[obj] = {}
            list_instances = objects_with_instances[obj]
            list_community_of_object = []
            for instance in list_instances:
                list_community_of_object.append(self.neo.get_community_from_instance(instance))
            for community in range(1, self.neo.number_of_communities + 1):
                if str(community) in list_community_of_object:
                    trust_objects_to_iot[obj][str(community)] = {}
                    instances_community = self.neo.get_instances_from_community(str(community))
                    occurrences = {}
                    for obj_instance in list_instances:
                        for instance in instances_community:
                            if (obj_instance, instance) in self.trust_repository:
                                for cff in self.trust_repository[(obj_instance, instance)]:
                                    if cff not in trust_objects_to_iot[obj][str(community)]:
                                        trust_objects_to_iot[obj][str(community)][cff] = 0.
                                        occurrences[cff] = 0
                                    trust_objects_to_iot[obj][str(community)][cff] = \
                                        trust_objects_to_iot[obj][str(community)][cff] + \
                                        self.trust_repository[(obj_instance, instance)][cff]
                                    occurrences[cff] = occurrences[cff] + 1
                    for cff in occurrences:
                        trust_objects_to_iot[obj][str(community)][cff] = trust_objects_to_iot[obj][str(community)][
                                                                             cff] / \
                                                                         occurrences[cff]
                else:
                    index_to_fill.append((obj, str(community)))
        # compute trust to iots from the point of view of objects that have no instance in those iots.
        for (obj, community_to_trust) in index_to_fill:
            list_instances = objects_with_instances[obj]
            trust_obj = {}
            occurrences = {}
            for instance in list_instances:
                trust_objects_to_iot[obj][community_to_trust] = {}
                mine_community = self.neo.get_community_from_instance(instance)
                for cff in self.overall_trust_iots[(mine_community, community_to_trust)]:
                    if cff in trust_objects_to_iot[obj][mine_community]:
                        if cff not in trust_objects_to_iot[obj][community_to_trust]:
                            trust_objects_to_iot[obj][community_to_trust][cff] = 0.
                            trust_obj[cff] = 0.
                            occurrences[cff] = 0
                        trust_obj[cff] = trust_obj[cff] + trust_objects_to_iot[obj][mine_community][cff] * \
                                         self.overall_trust_iots[(mine_community, community_to_trust)][cff]
                        occurrences[cff] = occurrences[cff] + 1
            for cff in trust_obj:
                trust_objects_to_iot[obj][community_to_trust][cff] = trust_obj[cff] / occurrences[cff]
        return trust_objects_to_iot

    def compute_overall_trust_iots(self):
        for comm_1 in range(1, self.neo.number_of_communities + 1):
            for comm_2 in range(1, self.neo.number_of_communities + 1):
                if comm_1 != comm_2:
                    objects_first_community = self.neo.get_objects_from_community(str(comm_1))
                    objects_second_community = self.neo.get_objects_from_community(str(comm_2))
                    self.overall_trust_iots[(str(comm_1), str(comm_2))] = self.compute_trust_iots(objects_first_community,
                                                                                                  objects_second_community)

    def compute_trust_iots(self, objects_iot_1, objects_iot_2):
        trust_iots = {}
        occurrences = {}
        for obj_iot_1 in objects_iot_1:
            for obj_iot_2 in objects_iot_2:
                if (obj_iot_1, obj_iot_2) in self.trust_object:
                    for cff in self.trust_object[(obj_iot_1, obj_iot_2)]:
                        if cff not in trust_iots:
                            trust_iots[cff] = 0.
                            occurrences[cff] = 0
                        trust_iots[cff] = trust_iots[cff] + self.trust_object[(obj_iot_1, obj_iot_2)][cff]
                        occurrences[cff] = occurrences[cff] + 1
        for cff in trust_iots:
            trust_iots[cff] = trust_iots[cff] / (occurrences[cff] + len(objects_iot_1))
        return trust_iots

    def compute_trust_objects(self):
        list_objects = self.neo.objects_with_instances
        for start_object in list_objects:
            for final_object in list_objects:
                if start_object != final_object:
                    sum_values = {}
                    occurrences = {}
                    start_object_instances = list_objects[start_object]
                    final_object_instances = list_objects[final_object]
                    for start_instance in start_object_instances:
                        for final_instance in final_object_instances:
                            if (start_instance, final_instance) in self.trust_repository:
                                for (context, file_format) in self.trust_repository[(start_instance, final_instance)]:
                                    if (context, file_format) not in sum_values:
                                        sum_values[(context, file_format)] = 0.
                                        occurrences[(context, file_format)] = 0
                                    sum_values[(context, file_format)] = sum_values[(context, file_format)] + \
                                                                         self.trust_repository[(start_instance, final_instance)][(context, file_format)]
                                    occurrences[(context, file_format)] = occurrences[(context, file_format)] + 1
                    if sum_values:
                        self.trust_object[(start_object, final_object)] = {}
                        for (context, file_format) in sum_values:
                            self.trust_object[(start_object, final_object)][(context, file_format)] = \
                                sum_values[(context, file_format)] / occurrences[(context, file_format)]
