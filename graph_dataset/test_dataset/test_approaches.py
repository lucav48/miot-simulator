from approaches import supervised_approach
from approaches import unsupervised_approach
from neo4JHandler import Neo4JManager
import settings
from tools import utilities


def get_fields_as_list_from_transactions(list_transactions, property_to_watch):
    context_result = []
    for t in list_transactions:
        context_result.append(getattr(t, property_to_watch))
    return context_result


def get_profile_couples_instances(list_transactions):
    profiles = {}
    for instances in list_transactions:
        profiles[instances] = {}
        for property_to_watch in settings.PROPERTY_TRANSACTION_TO_WATCH:
            analysis_results = get_fields_as_list_from_transactions(list_transactions[instances], property_to_watch)
            profiles[instances][property_to_watch] = utilities.u_plus_operator(analysis_results)
    return profiles


def get_profile_single_instance(profile_couples, instances):
    profile_single_instance = {}
    for instance in instances:
        profile_single_instance[instance.code] = {}
        couples = [key for key in profile_couples if key.split("-")[0] == instance.code
                   or key.split("-")[1] == instance.code]
        # for each property to watch
        for property_to_watch in settings.PROPERTY_TRANSACTION_TO_WATCH:
            # create dictionary for instance
            profile_single_instance[instance.code][property_to_watch] = {}
            for couple in couples:
                # for on property that is defined in couple profile (like {context: {'Music':1}})
                for single_property in profile_couples[couple][property_to_watch]:
                    if single_property in profile_single_instance[instance.code][property_to_watch]:
                        profile_single_instance[instance.code][property_to_watch][single_property] += \
                            profile_couples[couple][property_to_watch][single_property]
                    else:
                        profile_single_instance[instance.code][property_to_watch][single_property] = \
                            profile_couples[couple][property_to_watch][single_property]
    return profile_single_instance


def get_profile_single_object(profiles_instance, objects):
    profiles_single_object = {}
    for node in objects:
        profiles_single_object[node.code] = {}
        for prop in settings.PROPERTY_TRANSACTION_TO_WATCH:
            profiles_single_object[node.code][prop] = {}
            for single_instance in node.instances:
                if single_instance.code in profiles_instance:
                    for single_property in profiles_instance[single_instance.code][prop]:
                        if single_property in profiles_single_object[node.code][prop]:
                            profiles_single_object[node.code][prop][single_property] += \
                                profiles_instance[single_instance.code][prop][single_property]
                        else:
                            profiles_single_object[node.code][prop][single_property] = \
                                profiles_instance[single_instance.code][prop][single_property]
    return profiles_single_object


def content_based_analysis():
    transactions = neo.get_transactions()
    profile_content_couples_instances = get_profile_couples_instances(transactions)
    instances = neo.get_all_instances()
    profile_content_single_instance = get_profile_single_instance(profile_content_couples_instances, instances)
    objects = neo.get_all_objects()
    profile_content_single_object = get_profile_single_object(profile_content_single_instance, objects)
    return profile_content_single_instance, profile_content_single_object


def collaborative_filtering_analysis(profiles_instances):
    neighborhoods = neo.get_neighborhoods()
    p_collaborative_instances = {}
    for node in neighborhoods:
        p_collaborative_instances[node] = {}
        for prop in settings.PROPERTY_TRANSACTION_TO_WATCH:
            p_collaborative_instances[node][prop] = {}
            for single_instance in neighborhoods[node]:
                if p_collaborative_instances[node][prop]:
                    p_collaborative_instances[node][prop] = utilities.sum_occurrences_dict(
                        p_collaborative_instances[node][prop],
                        profiles_instances[single_instance.code][prop])
                else:
                    p_collaborative_instances[node][prop] = profiles_instances[single_instance.code][prop]
    objects = neo.get_all_objects()
    p_collaborative_object = get_profile_single_object(p_collaborative_instances, objects)
    return p_collaborative_instances, p_collaborative_object


def merge_profiles(content_based, collaborative_filtering):
    merged_profiles = {}
    for node in content_based:
        merged_profiles[node] = {}
        for characteristic in content_based[node]:
            if node in collaborative_filtering:
                merged_profiles[node][characteristic] = utilities.sum_occurrences_dict(content_based[node][characteristic],
                                                                                       collaborative_filtering[node][characteristic]
                                                                                       )
            else:
                # if node doesn't have a collaborative filtering profile, I have to add to that node only
                # the content based one.
                merged_profiles[node] = content_based[node]
    # if node has only collaborative filtering profile, it's not added in merged_profiles. I have to add it
    for node in collaborative_filtering:
        if node not in merged_profiles:
            merged_profiles[node] = collaborative_filtering[node]
    return merged_profiles


if __name__ == "__main__":
    neo = Neo4JManager.Neo4JManager()
    p_content_single_instance, p_content_single_object = content_based_analysis()
    p_collaborative_single_instance, p_collaborative_single_object = \
        collaborative_filtering_analysis(p_content_single_instance)
    p_overall_single_instance = merge_profiles(p_content_single_instance,
                                               p_collaborative_single_instance)
    p_overall_single_object = get_profile_single_object(p_overall_single_instance, neo.get_all_objects())
    if settings.SUPERVISED_APPROACH:
        supervised_approach.start(p_content_single_instance)
    else:
        unsupervised_approach.start()
