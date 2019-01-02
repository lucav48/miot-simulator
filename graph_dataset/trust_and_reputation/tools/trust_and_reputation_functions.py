from graph_dataset.trust_and_reputation import settings


def compute_trust_objects(list_objects, trust_repository):
    object_trust = {}
    for start_object in list_objects:
        for final_object in list_objects:
            if start_object != final_object:
                sum_values = {}
                occurrences = {}
                start_object_instances = list_objects[start_object]
                final_object_instances = list_objects[final_object]
                for start_instance in start_object_instances:
                    for final_instance in final_object_instances:
                        if (start_instance, final_instance) in trust_repository:
                            for (context, file_format) in trust_repository[(start_instance, final_instance)]:
                                if (context, file_format) not in sum_values:
                                    sum_values[(context, file_format)] = 0.
                                    occurrences[(context, file_format)] = 0
                                sum_values[(context, file_format)] = sum_values[(context, file_format)] +\
                                    trust_repository[(start_instance, final_instance)][(context, file_format)]
                                occurrences[(context, file_format)] = occurrences[(context, file_format)] + 1
                if sum_values:
                    object_trust[(start_object, final_object)] = {}
                    for (context, file_format) in sum_values:
                        object_trust[(start_object, final_object)][(context, file_format)] = \
                            sum_values[(context, file_format)] / occurrences[(context, file_format)]
    return object_trust


def compute_reputation_objects_in_miot(list_objects, trust_repository):
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
                behavioral_neighborhood = get_behavioral_neighborhood(instance, trust_repository.keys())
                for neighbor in behavioral_neighborhood:
                    if (neighbor, instance) in trust_repository:
                        for (context, file_format) in trust_repository[(neighbor, instance)]:
                            neighbor_object = neighbor.split(":")[0]
                            if (context, file_format) not in mean_values:
                                mean_values[(context, file_format)] = 0.
                                occurrences[(context, file_format)] = 0
                            if (context, file_format) not in actual_reputation[neighbor_object]:
                                actual_reputation[neighbor_object][(context, file_format)] = settings.INITIAL_REPUTATION_PAGERANK
                            mean_values[(context, file_format)] = mean_values[(context, file_format)] + \
                                trust_repository[(neighbor, instance)][(context, file_format)] * actual_reputation[neighbor_object][(context, file_format)]
                            occurrences[(context, file_format)] = occurrences[(context, file_format)] + 1
            for (context, file_format) in mean_values:
                mean_values[(context, file_format)] = settings.DAMPING_FACTOR +\
                                                      (1 - settings.DAMPING_FACTOR) * (mean_values[(context, file_format)] /
                                                                                       (occurrences[(context, file_format)] * len(obj_instances)))
            new_reputation[obj] = mean_values
        if is_converging(new_reputation, actual_reputation):
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
    return new_reputation


def is_converging(rep1, rep2):
    for obj in rep1:
        for context_file_format in rep1[obj]:
            if abs(rep1[obj][context_file_format] - rep2[obj][context_file_format]) > settings.CONVERGENCE_PAGERANK:
                return False
    return True


def get_contexts_used(trust_repository):
    list_context = []
    for instances in trust_repository:
        context_instances = trust_repository[instances].keys()
        for context_file_format in context_instances:
            if context_file_format not in list_context:
                list_context.append(context_file_format)
    return list_context


def get_behavioral_neighborhood(ins, pairwise_instances):
    neighborhood = []
    for (start_instance, final_instance) in pairwise_instances:
        if ins == start_instance:
            neighborhood.append(final_instance)
    return neighborhood


def compute_reputation_iot_in_miot(objects_with_instances, reputation_object, neo):
    number_of_communities = neo.number_of_communities
    reputation_iot = {}
    occurrences = {}
    for i in range(1, number_of_communities + 1):
        reputation_iot[str(i)] = {}
        occurrences[str(i)] = {}
    for obj in objects_with_instances:
        list_instances = objects_with_instances[obj]
        for instance in list_instances:
            instance_community = neo.get_community_from_instance(instance)
            for c_f_f in reputation_object[obj]:
                if c_f_f not in reputation_iot[instance_community]:
                    reputation_iot[instance_community][c_f_f] = 0.
                    occurrences[instance_community][c_f_f] = 0
                reputation_iot[instance_community][c_f_f] = reputation_iot[instance_community][c_f_f] + \
                                                            reputation_object[obj][c_f_f]
                occurrences[instance_community][c_f_f] = occurrences[instance_community][c_f_f] + 1
    for community in reputation_iot:
        for c_f_f in reputation_iot[community]:
            reputation_iot[community][c_f_f] = reputation_iot[community][c_f_f] / occurrences[community][c_f_f]
    return reputation_iot


def compute_trust_iots(objects_iot_1, objects_iot_2, trust_object):
    trust_iots = {}
    occurrences = {}
    for obj_iot_1 in objects_iot_1:
        for obj_iot_2 in objects_iot_2:
            if (obj_iot_1, obj_iot_2) in trust_object:
                for cff in trust_object[(obj_iot_1, obj_iot_2)]:
                    if cff not in trust_iots:
                        trust_iots[cff] = 0.
                        occurrences[cff] = 0
                    trust_iots[cff] = trust_iots[cff] + trust_object[(obj_iot_1, obj_iot_2)][cff]
                    occurrences[cff] = occurrences[cff] + 1
    for cff in trust_iots:
        trust_iots[cff] = trust_iots[cff] / (occurrences[cff] + len(objects_iot_1))
    return trust_iots


def compute_overall_trust_iots(neo, trust_objects):
    overall_trust_iots = {}
    for comm_1 in range(1, neo.number_of_communities + 1):
        for comm_2 in range(1, neo.number_of_communities + 1):
            if comm_1 != comm_2:
                objects_first_community = neo.get_objects_from_community(str(comm_1))
                objects_second_community = neo.get_objects_from_community(str(comm_2))
                overall_trust_iots[(str(comm_1), str(comm_2))] = compute_trust_iots(objects_first_community, objects_second_community, trust_objects)
    return overall_trust_iots


def compute_trust_object_to_iot(neo, objects_with_instances, trust_repository, overall_trust_iots):
    trust_objects_to_iot = {}
    index_to_fill = []
    for obj in objects_with_instances:
        trust_objects_to_iot[obj] = {}
        list_instances = objects_with_instances[obj]
        list_community_of_object = []
        for instance in list_instances:
            list_community_of_object.append(neo.get_community_from_instance(instance))
        for community in range(1, neo.number_of_communities + 1):
            if str(community) in list_community_of_object:
                trust_objects_to_iot[obj][str(community)] = {}
                instances_community = neo.get_instances_from_community(str(community))
                occurrences = {}
                for obj_instance in list_instances:
                    for instance in instances_community:
                        if (obj_instance, instance) in trust_repository:
                            for cff in trust_repository[(obj_instance, instance)]:
                                if cff not in trust_objects_to_iot[obj][str(community)]:
                                    trust_objects_to_iot[obj][str(community)][cff] = 0.
                                    occurrences[cff] = 0
                                trust_objects_to_iot[obj][str(community)][cff] = trust_objects_to_iot[obj][str(community)][cff] + \
                                                                                 trust_repository[(obj_instance, instance)][cff]
                                occurrences[cff] = occurrences[cff] + 1
                for cff in occurrences:
                    trust_objects_to_iot[obj][str(community)][cff] = trust_objects_to_iot[obj][str(community)][cff] / \
                                                                     occurrences[cff]
            else:
                index_to_fill.append((obj, str(community)))
    for (obj, community_to_trust) in index_to_fill:
        list_instances = objects_with_instances[obj]
        trust_obj = {}
        occurrences = {}
        for instance in list_instances:
            trust_objects_to_iot[obj][community_to_trust] = {}
            mine_community = neo.get_community_from_instance(instance)
            for cff in overall_trust_iots[(mine_community, community_to_trust)]:
                if cff in trust_objects_to_iot[obj][mine_community]:
                    if cff not in trust_objects_to_iot[obj][community_to_trust]:
                        trust_objects_to_iot[obj][community_to_trust][cff] = 0.
                        trust_obj[cff] = 0.
                        occurrences[cff] = 0
                    trust_obj[cff] = trust_obj[cff] + trust_objects_to_iot[obj][mine_community][cff] * \
                                     overall_trust_iots[(mine_community, community_to_trust)][cff]
                    occurrences[cff] = occurrences[cff] + 1
        for cff in trust_obj:
            trust_objects_to_iot[obj][community_to_trust][cff] = trust_obj[cff] / occurrences[cff]
    return trust_objects_to_iot
