from abc import ABC, abstractmethod


class FileManager(ABC):
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def write(self, record):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    