import json
import os

from file_format_converter.rules.numeric_rule import NumericRule
from file_format_converter.rules.string_length_rule import StringLengthRule
from file_format_converter.rules.url_rule import UrlRule

RULE_IMPLEMENTATIONS = {
    'str-length': StringLengthRule(),
    'numeric': NumericRule(),
    'url': UrlRule()
}


class RuleHelper:
    """
    This class loads the defined rules and use them to filter given row.
    """
    def __init__(self, rules_file, header_indexes):
        self.__rules_file = rules_file
        self.__header_indexes = header_indexes
        self.__rule_runner = self.__no_rules_apply
        self.__rules = {}

        try:
            if self.__rules_file and os.path.isfile(self.__rules_file):
                f = open(self.__rules_file, 'r')
                rules = json.load(f)
                if rules and len(rules) > 0:
                    self.__rules = rules
            else:
                print('Rules file is not found %s' % self.__rules_file)
        except Exception as e:
            print(e)
            print('Error loading rules file')

        valid_rule_definitions = {}
        for header_name in self.__rules:
            rule = self.__rules[header_name]
            valid_rule_definitions[header_name] = {}
            for rule_key in rule:
                rule_config = rule[rule_key]
                if rule_key in RULE_IMPLEMENTATIONS and hasattr(RULE_IMPLEMENTATIONS[rule_key], 'set_config'):
                    try:
                        RULE_IMPLEMENTATIONS[rule_key].set_config(rule_config)
                        valid_rule_definitions[header_name][rule_key] = rule_config
                    except Exception as e:
                        print(e)
                        print('Error initializing rule %s with config %s' % (rule, rule_config))
                else:
                    print('Unsupported rule key: %s' % rule_key)

        self.__rules = valid_rule_definitions

        if self.__rules and len(self.__rules) > 0:
            self.__rule_runner = self.__rules_apply

    def apply(self, row) -> (any, bool):
        """
        This method checks whether the row data conforms to the rules.

        :param row: single row data as list
        :return:
        """
        return self.__rule_runner(row)

    def __no_rules_apply(self, row) -> (any, bool):
        """
        This method do not apply any rule to given row.

        :param row: single row data as list
        :return: the row itself and True that means valid data
        """
        return row, True

    def __rules_apply(self, row) -> (any, bool):
        """
        This method apply the rules to given row.

        :param row: single row data as list
        :return: the row itself and bool that indicating whether the data in the row conforms to the rules
        """
        passed = True
        for header_name in self.__rules:  # each header rule set
            if header_name in self.__header_indexes:
                passed = True
                for rule in self.__rules[header_name]:  # each rule in rule set
                    passed = RULE_IMPLEMENTATIONS[rule].is_data_valid(row[self.__header_indexes[header_name]])
                    if not passed:
                        return row, False

        return row, passed
