from abc import ABC, abstractmethod


class Rule(ABC):
    def __init__(self):
        self.is_config_valid = True

    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def set_config(self, config) -> bool:
        pass

    @abstractmethod
    def is_data_valid(self, data) -> bool:
        pass
