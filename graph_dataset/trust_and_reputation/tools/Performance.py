import time
import matplotlib.pyplot as plt


class Performance:

    def __init__(self, neo):
        self.start_ts = 0
        self.neo = neo

    def set_start_ts(self):
        self.start_ts = time.time()

    def calculate_execution_time(self):
        print "Process lasted ", str(round(time.time() - self.start_ts, 2)), " seconds."

    def get_transactions_per_instance(self, reputation_repository, transactions):
        dict_instances = {}
        for community in reputation_repository:
            dict_instances[community] = {}
            for instance in reputation_repository[community]:
                dict_instances[community][instance] = 0
        for community in dict_instances:
            for instance in dict_instances[community]:
                for (start_instance, final_instance) in transactions:
                    if instance == start_instance:
                        for (context, file_format) in transactions[(start_instance, final_instance)]:
                            dict_instances[community][instance] = dict_instances[community][instance] + \
                                len(transactions[(start_instance, final_instance)][(context, file_format)])
        return dict_instances

    def print_transactions_for_instance(self, reputation_repository, transactions):
        transactions_per_ins = self.get_transactions_per_instance(reputation_repository, transactions)
        for community in transactions_per_ins:
            for instance in transactions_per_ins[community]:
                print instance, '# of transactions ', str(transactions_per_ins[community][instance]), " ", \
                    self.neo.list_instances[instance].precision_instance

    def plot_values_reputation(self, reputation_repository):
        # change key,value dictionary
        new_reputation = {}
        for community in reputation_repository:
            new_reputation[community] = {}
            for instance in reputation_repository[community]:
                for (context, file_format) in reputation_repository[community][instance]:
                    if (context, file_format) not in new_reputation[community]:
                        new_reputation[community][(context, file_format)] = {}
                    new_reputation[community][(context, file_format)][instance] = \
                        reputation_repository[community][instance][(context, file_format)]

        for community in new_reputation:
            if new_reputation[community]:
                i = 1
                n_rows = 2
                (n_cols, rest) = divmod(len(new_reputation[community]), n_rows)
                if rest != 0:
                    n_cols += 1
                plt.figure("Community " + str(community))
                for (context, file_format) in new_reputation[community]:
                    plt.subplot(n_rows, n_cols, i)
                    plt.gca().set_title("Context: " + context + " , " + " Format: " + file_format)
                    # plt.bar(range(len(transactions_per_ins[community])),
                    #         list(transactions_per_ins[community].values()),
                    #         width=0.5, align='center', color='red', label='# transactions')
                    plt.bar(range(len(new_reputation[community][(context, file_format)])),
                            list(new_reputation[community][(context, file_format)].values()),
                            width=0.5, align='edge', color='blue', label='Rep. score')
                    plt.xticks(range(len(new_reputation[community][(context, file_format)])),
                               list(new_reputation[community][(context, file_format)].keys()))
                    i += 1
        plt.show()

    def change_order(self, nested_dicts):
        n = {}
        for i in sorted(nested_dicts):
            for k, v in nested_dicts[i].items():
                if k not in n:
                    n[k] = [None] * len(nested_dicts)
                n[k][i] = v
        return n

    def statistics(self, list_transactions):
        num_success = 0.
        num_fail = 0.
        num_transactions = 0
        for transaction in list_transactions:
            for (context, file_format) in list_transactions[transaction]:
                transaction_to_watch = list_transactions[transaction][(context, file_format)]
                for tran in transaction_to_watch:
                    if tran.success == 1:
                        num_success += 1
                    else:
                        num_fail += 1
                    num_transactions += 1
        percentage_success = round(num_success / num_transactions, 3)
        percentage_failed = round(num_fail / num_transactions, 3)
        print "Percentage of transactions succeded: ", str(percentage_success)
        print "Percentage of transactions failed: ", str(percentage_failed)

    def print_trust(self, trust_repository):
        for (start_instance, final_instance) in trust_repository:
            print "\n", "Pairwise: ", (start_instance, final_instance), \
                "\t", trust_repository[(start_instance, final_instance)], \
                "Failure: ", self.neo.list_instances[start_instance].failure_rate_object

    def list_network_trusts(self, trustComputation, reputationComputation):
        trustComputation.compute_trust_objects()
        trustComputation.compute_overall_trust_iots()
        trustComputation.compute_trust_object_to_iot()
        reputationComputation.compute_reputation_objects_in_miot()
        reputationComputation.compute_reputation_iot_in_miot()
        print ""

    def mean_historical_values(self, values, file_name):
        f = open(file_name, "w")
        means = {}
        for index_1 in values:
            means[index_1] = 0.
            occurrences = 0
            for c_f_f in values[index_1]:
                for element in values[index_1][c_f_f]:
                    means[index_1] = means[index_1] + element
                    occurrences += 1
            means[index_1] = round(means[index_1] / occurrences,3)
            # print index_1, "\t", means[index_1]
        string_to_print = str(index_1) + "\t" + str(means[index_1]) + "\n"
        f.write(string_to_print)
        f.close()
        return means

    def mean_values(self, values, file_name):
        f = open(file_name, "w")
        means = {}
        for index_1 in values:
            means[index_1] = 0.
            occurrences = 0
            for c_f_f in values[index_1]:
                means[index_1] += values[index_1][c_f_f]
                occurrences += 1
            if occurrences > 0:
                means[index_1] = means[index_1] / occurrences
                string_to_print = str(index_1) + "\t" + str(means[index_1]) + "\n"
                f.write(string_to_print)
        f.close()
