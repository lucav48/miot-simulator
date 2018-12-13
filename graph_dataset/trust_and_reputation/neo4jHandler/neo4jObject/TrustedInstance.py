from graph_dataset.create_dataset.neo4JHandler.neo4JObject.Instance import Instance


class TrustedInstance(Instance):
    def __init__(self, i, selected_as_trust_repository):
        Instance.__init__(self, "", i["code"], i["community"])
        self.trust_repository = selected_as_trust_repository
