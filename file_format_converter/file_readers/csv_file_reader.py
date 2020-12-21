from _csv import reader

from file_format_converter.api.file_reader import FileReader


class CSVReader(FileReader):
    """
    This class read rows from csv file and yields them.
    """
    def __init__(self, __file_path):
        self.__file_path = __file_path
        self.__file = open(self.__file_path, 'r')

        self.__csv_reader = reader(self.__file)
        self.header = next(self.__csv_reader)

    def get_item_names(self):
        """
        Returns header row of the csv file.

        :return: header row as list
        """
        return self.header

    def get_items(self):
        """
        Yields all rows of csv file.

        :return: single row
        """
        for item in self.__csv_reader:
            yield item
