import json
import os

from file_format_converter.api.file_writer import FileWriter

from os import path


class JsonFileWriter(FileWriter):
    def __init__(self, config):
        super().__init__()
        self.__config = config

        self.__output_file = config.get("output", "output") + ".json"
        self.__file = open(self.__output_file, "w")
        self.__file.write("[")

    def close(self):
        self.__file.seek(self.__file.seek(0, os.SEEK_END) - 1)
        # self.__file.truncate()
        self.__file.write("]")
        self.__file.close()

    def get_result_location(self) -> str:
        return self.__output_file

    def save_item(self, data) -> bool:
        data_map = {}
        if self.header_index:
            for idx, val in enumerate(data):
                data_map[self.header_index[idx]] = val

        self.__file.write(json.dumps(data_map) + ",")

    def save(self, data) -> bool:
        pass
