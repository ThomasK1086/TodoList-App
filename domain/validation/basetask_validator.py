from domain.dtos.basetask import BaseTaskDTO
from utils.singleton import SingletonMetaclass
from abc import abstractmethod

class BaseTaskValidator(metaclass=SingletonMetaclass):

    @classmethod
    def validate(cls, task: BaseTaskDTO) -> bool:
        pass

