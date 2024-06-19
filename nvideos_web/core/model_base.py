from abc import ABC, abstractmethod

class ModelBase(ABC):

    @abstractmethod
    def create(self):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self):
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self):
        raise NotImplementedError()
