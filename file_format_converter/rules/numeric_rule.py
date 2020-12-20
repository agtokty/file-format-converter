from file_format_converter.api.rule import Rule


class NumericRule(Rule):
    def __init__(self):
        self.min = 0
        self.max = None

    def get_key(self) -> str:
        return 'numeric'

    def set_config(self, config={}) -> bool:
        min = config.get("min", None)
        max = config.get("max", None)

        if min is not None and isinstance(min, int):
            self.min = min

        if max is not None and isinstance(max, int):
            self.max = max

    def is_data_valid(self, data) -> bool:
        if data is None:
            return False
        if not isinstance(data, (int, float)):
            if isinstance(data, str):
                if not data.isdigit():
                    return False
                else:
                    data = float(data)

        if self.min and self.min > data:
            return False

        if self.max and self.max < data:
            return False

        return True
