from math import radians, cos, sin, asin, sqrt
import settings
import ast


def list_to_string(my_list):
    return ','.join(map(str, my_list))


def literal_eval(string):
    try:
        return ast.literal_eval(string)
    except ValueError:
        return []


def check_two_paths(big_path1, big_path2):
    connected = False
    for path in big_path1:
        if not connected:
            for other_path in big_path2:
                if not connected and two_points_are_close(path, other_path):
                    connected = True
    return connected


# point is a list [longitude, latitude]
def two_points_are_close(point1, point2):
    if haversine(point1[0], point1[1], point2[0], point2[1]) < settings.LIMIT_METER_CONNECTION:
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
