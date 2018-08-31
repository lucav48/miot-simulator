from math import radians, cos, sin, asin, sqrt
import graph_dataset.create_dataset.settings as settings
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
import ast
import time


def list_to_string(my_list):
    return ','.join(map(str, my_list))


def literal_eval(string):
    try:
        return ast.literal_eval(string)
    except ValueError:
        return []


# def check_two_paths(big_path1, big_path2):
#     connected = False
#     for path in big_path1:
#         if not connected:
#             for other_path in big_path2:
#                 if not connected and two_points_are_close(path, other_path):
#                     connected = True
#     return connected

def check_two_paths(big_path1, big_path2):
    points = nearest_points(big_path1, big_path2)
    return two_points_are_close([points[0].x, points[0].y], [points[1].x, points[1].y])


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


def write_to_file(neoManager):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_file = open(settings.PREFIX_DATASET_FILE + timestr + settings.CREATED_DATASET_EXTENSION, "w")

    # add objects
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_nodes_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # add objects
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_instances_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # add relationships
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_connections_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    # add transactions
    output_file.write(":begin\n")
    output_file.write(neoManager.neo4j_create_transactions_query.encode('utf-8'))
    output_file.write("\n:commit\n")
    output_file.close()


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
            final_travel.append(Point(new_travel))
        else:
            final_travel.append(LineString(new_travel))
    return final_travel


def check_numbers(num1, num2):
    if complex(num1) and complex(num2):
        return True
    else:
        return False
