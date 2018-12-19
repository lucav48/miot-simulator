import time
import matplotlib.pyplot as plt


class Performance:

    def __init__(self):
        self.start_ts = 0

    def set_start_ts(self):
        self.start_ts = time.time()

    def calculate_execution_time(self):
        print "Process lasted ", str(time.time() - self.start_ts), " seconds."

    def plot_values(self, reputation_repository):
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
                    plt.bar(range(len(new_reputation[community][(context, file_format)])),
                            list(new_reputation[community][(context, file_format)].values()), align='center')
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
