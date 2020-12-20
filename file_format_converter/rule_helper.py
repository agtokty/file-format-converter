import json
import os


class RuleHelper:
    def __init__(self, rules_file, header_indexes):
        self.__rules_file = rules_file
        self.__header_indexes = header_indexes
        self.__rule_runner = self.__no_rules_apply
        self.__rules = {}

        try:
            if self.__rules_file and os.path.isfile(self.__rules_file):
                f = open(self.__rules_file, 'r')
                self.__rules = json.load(f)
        except:
            print('Error loading rules file')

    def apply(self, row) -> (any, bool):
        return self.__rule_runner(row)

    def __no_rules_apply(self, row) -> (any, bool):
        return row, True

    def __rules_apply(self, row) -> (any, bool):
        return row, True
