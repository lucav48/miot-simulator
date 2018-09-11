from graph_dataset.test_dataset import settings as settings


def u_plus_operator(items):
    counting_list = {}
    for item in items:
        if item in counting_list:
            counting_list[item] += 1
        else:
            counting_list[item] = 1
    return counting_list


def sum_occurrences_dict(list1, list2):
    results = {}
    for key in list1:
        results[key] = list1[key]
        if key in list2:
            results[key] += list2[key]
    for key in list2:
        if key not in results:
            results[key] = list2[key]
    return results


def define_q_first():
    q_first = {}
    for key in settings.TOPIC_SUPERVISED_APPROACH:
        q_first[key] = 1
    return q_first


def sum_occurrences(list_to_sum):
    sum_list = 0
    for key in list_to_sum:
        sum_list += float(list_to_sum[key])
    return sum_list


def intersect_dict(dict1, dict2):
    result_dict = {}
    for key in dict1:
        if key in dict2:
            result_dict[key] = float(dict1[key]) + float(dict2[key])
    return result_dict


def jaccard_star(topicset1, topicset2):
    common_ts = intersect_dict(topicset1, topicset2)
    num = sum_occurrences(common_ts)
    den = (sum_occurrences(topicset1) + sum_occurrences(topicset2))
    tot = num / den
    return tot
