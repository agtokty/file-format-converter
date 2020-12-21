import unittest

from file_format_converter.rules.string_length_rule import StringLengthRule


def fun(x):
    return x + 1


TEST_DATA_HEADERS = ["name", "address", "stars", "contact", "phone", "url"]
TEST_DATA = ["The Gibson", "63847 Lowe Knoll, East Maxine, WA 97030-4876", "5", "Dr. Sinda Wyman", "1-270-665-9933x1626", "http://www.paucek.com/search.htm"]


class RuleTests(unittest.TestCase):

    def __init__(self):
        self.string_length_rule = StringLengthRule();

    def test_string_length_empty_config(self):
        self.string_length_rule.set_config({})
        self.assertEqual(self.string_length_rule.is_data_valid("test string"), True)

    def test_string_length_only_min(self):
        self.string_length_rule.set_config({min: 5})
        self.assertEqual(self.string_length_rule.is_data_valid("test string"), True)
        self.assertEqual(self.string_length_rule.is_data_valid("test"), False)

    def test_string_length_only_max(self):
        self.string_length_rule.set_config({max: 5})
        self.assertEqual(self.string_length_rule.is_data_valid("test string"), False)
        self.assertEqual(self.string_length_rule.is_data_valid("test"), True)
        self.assertEqual(self.string_length_rule.is_data_valid("test1"), True)

    def test_string_length_min_max(self):
        self.string_length_rule.set_config({max: 5, min: 3})
        self.assertEqual(self.string_length_rule.is_data_valid("test string"), False)
        self.assertEqual(self.string_length_rule.is_data_valid("test"), True)
        self.assertEqual(self.string_length_rule.is_data_valid("test1"), True)
        self.assertEqual(self.string_length_rule.is_data_valid("te"), False)
        self.assertEqual(self.string_length_rule.is_data_valid("tes"), True)
