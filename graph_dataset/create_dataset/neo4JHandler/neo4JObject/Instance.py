class Instance:
    def __init__(self, path, code, num_community):
        self.travel_path = path
        self.code = code
        self.community = str(num_community)

    def instance_as_string(self):
        return "code:'" + self.code + "',community:'" + self.community + "'"
