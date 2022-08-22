import abc

class Table(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def write(self):
        pass

    @abc.abstractmethod
    def create_columns(self):
        pass

    @abc.abstractmethod
    def is_not_columns(self):
        pass

    @classmethod
    def get_columns(cls):
        columns = [
            'title', 
            'part_of_speech', 
            'us_pronunciation', 
            'uk_pronunciation', 
            'definition', 
            'example_sentence', 
            'timestamp']
        return columns