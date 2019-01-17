import time


class TransactionsComputation:

    def __init__(self, neo):
        self.neo = neo
        self.list_transactions = {}
        self.maxNumTranSet = {}
        self.maxSize = {}
        self.first_ts = {}
        self.setup_maxnumtranset_and_maxsize()

    def update_maxsize_and_maxnumtranset(self, community, context, file_format, number_of_transactions, new_size,  success_transaction):
        if success_transaction == 1:
            if (context, file_format) not in self.maxNumTranSet[community]:
                self.maxNumTranSet[community][(context, file_format)] = number_of_transactions
            else:
                if self.maxNumTranSet[community][(context, file_format)] < number_of_transactions:
                    self.maxNumTranSet[community][(context, file_format)] = number_of_transactions

        if (context, file_format) not in self.maxSize[community]:
            self.maxSize[community][(context, file_format)] = new_size
        else:
            if new_size > self.maxSize[community][(context, file_format)]:
                self.maxSize[community][(context, file_format)] = new_size

    def setup_maxnumtranset_and_maxsize(self):
        for i in range(1, self.neo.number_of_communities + 1):
            self.maxNumTranSet[str(i)] = {}
            self.maxSize[str(i)] = {}

    def add_new_transaction(self, code, start_instance, final_instance, context, file_format, size):
        start_code = start_instance.code
        finish_code = final_instance.code
        new_transaction = self.neo.generate_transaction(code, start_code, finish_code,
                                                        context, file_format, size, start_instance.precision_instance)
        if (start_code, finish_code) not in self.list_transactions:
            self.list_transactions[(start_code, finish_code)] = {}
            self.list_transactions[(start_code, finish_code)][(context, file_format)] = [new_transaction]
        else:
            if (context, file_format) not in self.list_transactions[(start_code, finish_code)]:
                self.list_transactions[(start_code, finish_code)][(context, file_format)] = [new_transaction]
            else:
                self.list_transactions[(start_code, finish_code)][(context, file_format)].append(new_transaction)
        # update first ts
        if start_instance not in self.first_ts:
            self.first_ts[start_code] = time.time()
        number_transactions = len(self.list_transactions[(start_instance.code, final_instance.code)][(context, file_format)])
        self.update_maxsize_and_maxnumtranset(start_instance.community, context, file_format, number_transactions,
                                              size, new_transaction.success)
