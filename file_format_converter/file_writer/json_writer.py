import json
import os

from file_format_converter.api.file_writer import FileWriter

from os import path


class JsonFileWriter(FileWriter):
    def __init__(self, config):
        super().__init__()
        self.__config = config

        self.__formatted = self.__config.get("formatted", True)
        self.__output_file = config.get("output", "output") + ".json"

        self.item_adder = self.__no_formatted_item_adder
        if self.__config.get("formatted", True):
            self.item_adder = self.__formatted_item_adder

        self.__file = open(self.__output_file, "w")
        self.__file.write("[")

    def close(self):
        self.__file.seek(self.__file.seek(0, os.SEEK_END) - 1)
        self.__file.write("]")
        self.__file.close()

    def get_result_location(self) -> str:
        return self.__output_file

    def save_item(self, item):
        data_map = {}
        if self.header_index:
            for idx, val in enumerate(item):
                data_map[self.header_index[idx]] = val
        self.item_adder(data_map)

    def __no_formatted_item_adder(self, data_map):
        self.__file.write(json.dumps(data_map) + ",")

    def __formatted_item_adder(self, data_map):
        self.__file.write("\n" + json.dumps(data_map, indent=4) + ",")

    def save(self, data) -> bool:
        pass
