from graph_dataset.create_dataset import settings
from math import radians, cos, sin, asin, sqrt
import csv
import json


def read_csv(path_csv_file):
    read_rows = {}
    csv_file = open(path_csv_file, 'r')
    reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in reader:
        if row[-1] != '[]' and i > 0:
            read_rows[i] = string_to_list(row[-1])
            i += 1
        if i == 0:
            i += 1
    return read_rows


def string_to_list(string):
    listone = []
    new_string = string.replace("[", "").replace("]", "")
    coords = new_string.split(",")
    for i in range(0, len(coords), 2):
        if i+1 < len(coords):
            new_coords = [float(coords[i]), float(coords[i+1])]
            listone.append(new_coords)
    return listone


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


def min_distance(path1, path2):
    distance = 100000
    for [lot1, lat1] in path1:
        for [lot2, lat2] in path2:
            d_haversine = haversine(lot1, lat1, lot2, lat2)
            if d_haversine < distance:
                distance = d_haversine
    return distance


if __name__ == "__main__":
    rows = read_csv("../../" + settings.TRAVEL_CSV)
    distances = {}
    for path in [1,2]:
        distances[path] = {}
        for other_path in range(path + 1, len(rows.keys())):
            if path != other_path:
                distances[path][other_path] = min_distance(rows[path], rows[other_path])
        print(path)
    json.dump(distances, open("../../" + settings.TRAVEL_JSON, 'w'))
    # d2 = json.load(open("json_path.txt"))
