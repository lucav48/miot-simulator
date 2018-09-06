from math import radians, cos, sin, asin, sqrt
import graph_dataset.create_dataset.settings as settings
import ast
import time
import numpy as np
import pandas


def list_to_string(my_list):
    return ','.join(map(str, my_list))


def literal_eval(string):
    try:
        return ast.literal_eval(string)
    except ValueError:
        return []


def check_two_paths_every_point(big_path1, big_path2):
    for [lon1, lat1] in big_path1.values:
        for [lon2, lat2] in big_path2.values:
            if haversine(lon1, lat1, lon2, lat2) < settings.LIMIT_METER_CONNECTION:
                return True
    return False


def check_two_paths_entire_way(big_path1, big_path2):
        # check paths like they are moving together
        distances = haversine_np(big_path1['lon'], big_path1['lat'],
                                 big_path2['lon'], big_path2['lat'])
        if np.nanmin(distances.values) < settings.LIMIT_METER_CONNECTION:
            return True
        else:
            return False


def check_two_paths(big_path1, big_path2):
    if settings.CHECK_EVERY_POINT:
        # check every point of first path to entire second path
        return check_two_paths_every_point(big_path1, big_path2)
    else:
        return check_two_paths_entire_way(big_path1, big_path2)


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    meters = 6367 * c * 1000

    return meters


# point is a list [longitude, latitude]
def two_points_are_close(lot1, lat1, lot2, lat2):
    if haversine(lot1, lat1, lot2, lat2) < settings.LIMIT_METER_CONNECTION:
        return True
    else:
        return False


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
    # Radius of earth in kilometers is 6371
    meters = 6371 * 1000 * c
    return meters


def prepare_travel_array(list_travel):
    final_travel = []
    for travel in list_travel:
        new_travel = []
        app_travel = travel[1:-1].replace("[", "").replace("]", "").split(",")
        for i in range(0, len(app_travel), 2):
            try:
                if check_numbers(app_travel[i], app_travel[i+1]):
                    new_travel.append((float(app_travel[i]), float(app_travel[i+1])))
            except IndexError:
                continue
        if len(new_travel) == 1:
            final_travel.append(new_travel)
        else:
            final_travel.append(new_travel)
    return final_travel


def check_numbers(num1, num2):
    if complex(num1) and complex(num2):
        return True
    else:
        return False


def travel_to_dataframe(travel):
    lon = []
    lat = []
    for element in travel:
        lon.append(element[0])
        lat.append(element[1])
    return pandas.DataFrame(data={'lon': lon, 'lat': lat})


def print_date():
    print "Script started at " + time.strftime("%H:%M:%S")
