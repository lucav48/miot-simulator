from graph_dataset.test_dataset.tools import utilities
from graph_dataset.test_dataset import settings


def start(profile_instances):
    print("Supervised approach started!")
    q_first = utilities.define_q_first()
    ci = build_ci(profile_instances, q_first)
    ri = build_ri(ci, q_first)
    print len(ri)


def build_ri(ci, q_first):
    ri = {}
    for instance in ci:
        j_star = utilities.jaccard_star(ci[instance], q_first)
        if j_star > settings.THRESHOLD_SUPERVISED:
            ri[instance] = ci[instance]
    return ri


def build_ci(instances, q_first):
    ci = {}
    con = settings.TRANSACTION_CONTEXT_FIELD
    for supervised_key in q_first:
        for instance in instances:
            if supervised_key in instances[instance][con]:
                ci[instance] = instances[instance][con]
    return ci
