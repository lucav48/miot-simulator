import geocoding_for_kml
import csv
import xml.dom.minidom
import sys
from graph_dataset.create_dataset import settings

def createPlacemark(kmlDoc, coor):
    # This creates a  element for a row of data.
    # A row is a dict.
    placemarkElement = kmlDoc.createElement('Placemark')
    pointElement = kmlDoc.createElement('Point')
    placemarkElement.appendChild(pointElement)
    coordinates = coor
    coorElement = kmlDoc.createElement('coordinates')
    coorElement.appendChild(kmlDoc.createTextNode(coordinates))
    pointElement.appendChild(coorElement)
    return placemarkElement


def createKML(csvReader, fileName):
    # This constructs the KML document from the CSV file.
    kmlDoc = xml.dom.minidom.Document()

    kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
    kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
    kmlElement = kmlDoc.appendChild(kmlElement)
    documentElement = kmlDoc.createElement('Document')
    documentElement = kmlElement.appendChild(documentElement)

    # Skip the header line.
    csvReader.next()
    csvReader.next()

    i = 0
    for row in csvReader:
        if i < 200:
            route = get_route(row['POLYLINE'])
            for coor in route:
                placemarkElement = createPlacemark(kmlDoc, coor)
                documentElement.appendChild(placemarkElement)
            i += 1
    kmlFile = open(fileName, 'w')
    kmlFile.write(kmlDoc.toprettyxml('  ', newl='\n', encoding='utf-8'))

def get_route(polyline_string):
    polyline = polyline_string.split("],")
    placemarks = []
    for line in polyline:
        line = line.replace("[", "")
        line = line.replace(" ", "")
        lon, lat = line.split(",")
        place = lon + ", " + lat
        placemarks.append(place)
    return placemarks

def main():
    # This reader opens up 'google-addresses.csv', which should be replaced with your own.
    # It creates a KML file called 'google.kml'.

    # If an argument was passed to the script, it splits the argument on a comma
    # and uses the resulting list to specify an order for when columns get added.
    # Otherwise, it defaults to the order used in the sample.

    csvreader = csv.DictReader(open("../../" + settings.TRAVEL_CSV))
    createKML(csvreader, 'google-addresses.kml')


if __name__ == '__main__':
    main()
