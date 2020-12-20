from abc import ABC, abstractmethod


class FileWriter(ABC):
    def __init__(self):
        self.is_config_valid = True
        self.header_index = {}

    def set_header(self, header_index):
        self.header_index = header_index

    @abstractmethod
    def get_result_location(self) -> str:
        pass

    @abstractmethod
    def save_item(self, line) -> bool:
        pass

    @abstractmethod
    def close(self, item):
        pass
