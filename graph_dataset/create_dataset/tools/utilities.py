import time
from math import radians, cos, sin, asin, sqrt


def list_to_string(my_list, separator=","):
    return separator.join(map(str, my_list))


def print_date(string):
    print "Script " + string + " at " + time.strftime("%H:%M:%S")


def string_to_path(travel_string):
    travel_path = []
    string_to_list = travel_string.split("],")
    for x in string_to_list:
        x = x.replace("[", "").replace(" ", "").replace("]", "")
        lon, lat = x.split(",")
        travel_path.append((float(lon), float(lat)))
    return travel_path


def calculate_haversine(travel_path, (lat2, lot2)):
    min_distance = 10000
    for (lot1, lat1) in travel_path:
        distance = haversine(lot1, lat1, lot2, lat2)
        if distance < min_distance:
            min_distance = distance
    return min_distance


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    meters = 6367 * c * 1000
    return meters
