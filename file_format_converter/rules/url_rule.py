from file_format_converter.api.rule import Rule
import re


class UrlRule(Rule):
    def __init__(self):
        self.regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def get_key(self) -> str:
        return 'url'

    def set_config(self, config={}) -> bool:
        pass

    def is_data_valid(self, data) -> bool:
        if data is None:
            return False

        return re.match(self.regex, data) is not None
