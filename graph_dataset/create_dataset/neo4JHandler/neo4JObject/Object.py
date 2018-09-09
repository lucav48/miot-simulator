from graph_dataset.create_dataset.tools import utilities


class Object:
    def __init__(self, des, tec, code, instances, n_instances):
        self.descriptive = des
        self.technical = tec
        self.code = code
        self.instances = instances
        self.num_instances = n_instances

    def object_as_string(self):
        return "descriptive:'" + utilities.list_to_string(self.descriptive) \
                + "', technical:'" + utilities.list_to_string(self.technical) \
                + "', code:'" + self.code + "'"