from abc import ABCMeta, abstractmethod


class ModelBase(metaclass=ABCMeta):
    @abstractmethod
    def take_action(self, info):
        pass

    @abstractmethod
    def update_param(self, new_param):
        pass

    @abstractmethod
    def param_vector(self):
        pass

    def __str__(self):
        return str(self.param_vector())
