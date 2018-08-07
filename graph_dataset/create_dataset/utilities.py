from math import radians, cos, sin, asin, sqrt
import settings


def list_to_string(my_list):
    return ','.join(map(str, my_list))


def two_paths_are_close(path1, path2):
    if haversine(path1[0], path1[1], path2[0], path2[1]) < settings.LIMIT_METER_CONNECTION:
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
