import graph_dataset.create_dataset.settings as settings
import utilities
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
        self.context_dict = dict()

    def read_all(self):
        # read all from file
        self.descriptive_array = self.read_file(self.descriptive_path_file)
        self.technical_array = self.read_file(self.technical_path_file)
        travels = self.read_file(self.travel_path_file)
        # delete first row that is the table caption
        travels.pop(0)
        self.travel_array = utilities.prepare_travel_array(travels)
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
        items = mydoc.getElementsByTagName('row')[0:settings.NUMBER_OF_CONTENT_MESSAGES_TO_READ]
        return items
        # print items[8954].attributes["Id"].value

    def read_file_csv(self, path_csv_file):
        read_rows = []
        csv_file = open(path_csv_file, 'r')
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if path_csv_file == settings.TRAVEL_CSV:
                if row[-1] != '[]':
                    read_rows.append(row[-1])
            else:
                read_rows.append(row)
        return read_rows

    def read_all_context(self, context):
        for c in context:
            path = settings.CONTEXT_FOLDER + "/" + c + settings.SUFFIX_CONTEXT_FILE
            self.context_dict[c] = self.read_file_xml(path)
