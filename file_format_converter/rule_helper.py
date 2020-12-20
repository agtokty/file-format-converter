import json
import os

from file_format_converter.rules.string_length_rule import StringLengthRule

RULE_IMPLEMENTATIONS = {
    "str-length": StringLengthRule()
}


class RuleHelper:
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
        except:
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
                    except:
                        print('Error initializing rule %s with config %s' % (rule, rule_config))
                else:
                    print('Unsupported rule key: %s' % rule_key)

        self.__rules = valid_rule_definitions

        if self.__rules and len(self.__rules) > 0:
            self.__rule_runner = self.__rules_apply

    def apply(self, row) -> (any, bool):
        return self.__rule_runner(row)

    def __no_rules_apply(self, row) -> (any, bool):
        return row, True

    def __rules_apply(self, row) -> (any, bool):
        result = row
        passed = True
        for header_name in self.__rules:  # each header rule set
            if header_name in self.__header_indexes:
                passed = True
                for rule in self.__rules[header_name]:  # each rule in rule set
                    passed = RULE_IMPLEMENTATIONS[rule].is_data_valid(row[self.__header_indexes[header_name]])
                    if not passed:
                        return result, False

        return result, passed
