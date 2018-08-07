import ReadFile
import Neo4JManager
import settings
import random
import ast
import utilities


def create_nodes(readFile):
    i = 0
    list_nodes = []
    travel_already_chosen = []
    while i < settings.NUMBER_OF_NODES:
        new_node = []
        new_node.append(random.choice(readFile.descriptive_array))
        new_node.append(random.choice(readFile.technical_array))
        # travel has to be unique among nodes
        new_travel = random.choice(readFile.travel_array)
        while new_travel in travel_already_chosen:
            new_travel = random.choice(readFile.travel_array)
        new_node.append(new_travel)
        travel_already_chosen.append(new_travel)
        new_node.append(str(i))
        list_nodes.append(new_node)
        i += 1
    return list_nodes


def create_connections(list_nodes):
    i = 0
    n_nodes = len(list_nodes)
    while i < n_nodes:
        node = list_nodes[i]
        j = i + 1
        while j < n_nodes:
            node_path = ast.literal_eval(node[2])
            other_node = list_nodes[j]
            other_node_path = ast.literal_eval(other_node[2])
            connected = False
            for path in node_path:
                for other_path in other_node_path:
                    if utilities.two_paths_are_close(path, other_path) and not connected:
                        neoManager.neo4j_create_connection(node[3], other_node[3])
                        connected = True
            j += 1
        i += 1


if __name__ == "__main__":
    # read data useful to create nodes
    readFile = ReadFile.ReadFile()
    neoManager = Neo4JManager.Neo4JManager()
    readFile.read_all()
    # create a list of nodes
    nodes = create_nodes(readFile)
    # write neo4j queries to represent those nodes
    neoManager.neo4j_create_nodes(nodes)
    # look for connections among nodes and represent it as neo4j query
    create_connections(nodes)
    print neoManager.neo4j_nodes_query
