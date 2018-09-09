

def u_plus_operator(items):
    counting_list = {}
    for item in items:
        if item in counting_list:
            counting_list[item] += 1
        else:
            counting_list[item] = 1
    return counting_list


def sum_profiles(list1, list2):
    results = {}
    for key in list1:
        results[key] = list1[key]
        if key in list2:
            results[key] += list2[key]
    for key in list2:
        if key not in results:
            results[key] = list2[key]
    return results
