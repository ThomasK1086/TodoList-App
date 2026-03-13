from dataclasses import dataclass
import datetime

from utils.singleton import SingletonMetaclass


@dataclass(init=False, frozen=True, repr=False, order=False)
class BaseTaskDTO:
    id: int
    group_id: int
    task_type: str
    title: str
    created_at: datetime.date


class BaseTaskFactory(metaclass=SingletonMetaclass):
    def create(self, *args, **kwargs) -> BaseTaskDTO:
        ...

    def __call__(self, *args, **kwargs) -> BaseTaskDTO:
        return self.create(*args, **kwargs)
