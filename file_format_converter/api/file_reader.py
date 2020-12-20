from abc import ABC, abstractmethod


class FileReader(ABC):
    def __init__(self):
        self.is_config_valid = True

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_item_names(self):
        pass
