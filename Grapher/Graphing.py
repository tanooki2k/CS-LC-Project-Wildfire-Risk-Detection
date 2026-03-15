from abc import ABC, abstractmethod

class MatplotlibGraph(ABC):
    @abstractmethod
    def new_record(self, record):
        pass

    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def show(self, record=None, can_save:bool=False):
        pass

    @staticmethod
    @abstractmethod
    def save(path):
        pass
