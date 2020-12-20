import json
import os

from file_format_converter.api.file_writer import FileWriter

from os import path


class XmlFileWriter(FileWriter):
    def __init__(self, config):
        super().__init__()
        self.__config = config

        self.__output_file = self.__config.get("output", "output") + ".xml"
        self.__formatted = self.__config.get("formatted", True)
        self.__item_tag = self.__config.get("tag", "item")
        self.__item_parent_tag = self.__config.get("parent_tag", self.__item_tag + "s")

        self.item_adder = self.__no_formatted_item_adder
        if self.__config.get("formatted", True):
            self.item_adder = self.__formatted_item_adder

        self.__file = open(self.__output_file, "w")

        self.__file.write("<%s>" % self.__item_parent_tag)
        if self.__formatted:
            self.__file.write("\n")

    def close(self):
        self.__file.write("</%s>" % self.__item_parent_tag)
        self.__file.close()

    def get_result_location(self) -> str:
        return self.__output_file

    def save_item(self, data):
        self.item_adder(data)

    def __formatted_item_adder(self, item):
        if self.header_index:
            self.__file.write("\t<%s>\n" % self.__item_tag)

            for idx, val in enumerate(item):
                item_property = self.header_index[idx]
                line = "\t\t<%s>%s</%s>\n" % (item_property, val, item_property)
                self.__file.write(line)

            self.__file.write("\t</%s>\n" % self.__item_tag)

    def __no_formatted_item_adder(self, item):
        if self.header_index:
            self.__file.write("\t<%s>\n" % self.__item_tag)

            for idx, val in enumerate(item):
                item_property = self.header_index[idx]
                line = "<%s>%s</%s>" % (item_property, val, item_property)
                self.__file.write(line)

            self.__file.write("\t</%s>\n" % self.__item_tag)

    def save(self, data) -> bool:
        pass
