from graph_dataset.trust_and_reputation import settings


class TrustComputation:

    def __init__(self, neo, transaction_computation_instance):
        self.neo = neo
        self.trust_repository = {}
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
        self.trust_repository[(start_instance, final_instance)][(context, file_format)] = trust_instances

    def get_trust_instances(self, ins_start, ins_finish, context, file_format):
        found = False
        trust = settings.INITIAL_TRUST_VALUE
        if (ins_finish, ins_start) in self.trust_repository:
            if (context, file_format) in self.trust_repository[(ins_finish, ins_start)]:
                found = True
                trust = self.trust_repository[(ins_finish, ins_start)][(context, file_format)]
        if not found:
            if (ins_finish, ins_start) not in self.trust_repository:
                self.trust_repository[(ins_finish, ins_start)] = {}
                self.trust_repository[(ins_finish, ins_start)][(context, file_format)] = trust
        return trust
