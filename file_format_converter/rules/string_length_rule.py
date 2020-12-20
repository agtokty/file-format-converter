from file_format_converter.api.rule import Rule


class StringLengthRule(Rule):
    def __init__(self):
        self.len_min = 0
        self.len_max = None

    def get_key(self) -> str:
        return 'str-length'

    def set_config(self, config={}) -> bool:
        len_min = config.get("min", None)
        len_max = config.get("max", None)

        if len_min is not None and isinstance(len_min, int):
            self.len_min = len_min

        if len_max is not None and isinstance(len_max, int):
            self.len_max = len_max

    def is_data_valid(self, data) -> bool:
        data_len = len(data)

        if self.len_min and self.len_min > data_len:
            return False

        if self.len_max and self.len_max < data_len:
            return False

        return True
