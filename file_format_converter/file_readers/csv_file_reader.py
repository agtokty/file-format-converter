from _csv import reader

from file_format_converter.api.file_reader import FileReader


class CSVReader(FileReader):

    def __init__(self, __file_path):
        self.__file_path = __file_path
        self.__file = open(self.__file_path, 'r')

        self.__csv_reader = reader(self.__file)
        self.header = next(self.__csv_reader)

    def get_item_names(self):
        return self.header

    def get_items(self):
        for item in self.__csv_reader:
            yield item
