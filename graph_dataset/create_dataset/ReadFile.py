import settings
import csv
from xml.dom import minidom


class ReadFile:

    def __init__(self):
        self.descriptive_path_file = settings.DESCRIPTIVE_CSV
        self.technical_path_file = settings.TECHNICAL_CSV
        self.travel_path_file = settings.TRAVEL_CSV
        # data from files
        self.descriptive_array = []
        self.technical_array = []
        self.travel_array = []
        # header of read file
        self.descriptive_header = []
        self.technical_header = []

    def read_all(self):
        # read all from file
        self.descriptive_array = self.read_file(self.descriptive_path_file)
        self.technical_array = self.read_file(self.technical_path_file)
        self.travel_array = self.read_file(self.travel_path_file)
        # get only header of data
        self.descriptive_header = self.descriptive_array[0]
        del self.descriptive_array[0]
        self.technical_header = self.technical_array[0]
        del self.technical_array[0]

    def read_file(self, path_file):
        extension = path_file.split(".")[1]
        if extension == "csv":
            return self.read_file_csv(path_file)
        elif extension == "xml":
            return self.read_file_xml(path_file)

    def read_file_xml(self, path_xml_file):
        mydoc = minidom.parse(path_xml_file)
        items = mydoc.getElementsByTagName('row')
        return items
        # print items[8954].attributes["Id"].value

    def read_file_csv(self, path_csv_file):
        read_rows = []
        csv_file = open(path_csv_file, 'r')
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if path_csv_file == settings.TRAVEL_CSV:
                read_rows.append(row[8])
            else:
                read_rows.append(row)
        return read_rows
